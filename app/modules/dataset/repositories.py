from datetime import datetime, timezone
import logging
from flask_login import current_user
from typing import Optional

from sqlalchemy import desc, func

from app.modules.dataset.models import (
    Author,
    DOIMapping,
    DSDownloadRecord,
    DSMetaData,
    DSViewRecord,
    DataSet, 
    Rating
)
from core.repositories.BaseRepository import BaseRepository

logger = logging.getLogger(__name__)


class AuthorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Author)


class DSDownloadRecordRepository(BaseRepository):
    def __init__(self):
        super().__init__(DSDownloadRecord)

    def total_dataset_downloads(self) -> int:
        max_id = self.model.query.with_entities(func.max(self.model.id)).scalar()
        return max_id if max_id is not None else 0


class DSMetaDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(DSMetaData)

    def filter_by_doi(self, doi: str) -> Optional[DSMetaData]:
        return self.model.query.filter_by(dataset_doi=doi).first()


class DSViewRecordRepository(BaseRepository):
    def __init__(self):
        super().__init__(DSViewRecord)

    def total_dataset_views(self) -> int:
        max_id = self.model.query.with_entities(func.max(self.model.id)).scalar()
        return max_id if max_id is not None else 0

    def the_record_exists(self, dataset: DataSet, user_cookie: str):
        return self.model.query.filter_by(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset.id,
            view_cookie=user_cookie
        ).first()

    def create_new_record(self, dataset: DataSet, user_cookie: str) -> DSViewRecord:
        return self.create(
                user_id=current_user.id if current_user.is_authenticated else None,
                dataset_id=dataset.id,
                view_date=datetime.now(timezone.utc),
                view_cookie=user_cookie,
            )


class DataSetRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)
        self.rating_repository = DatasetRatingRepository() #AÑADIDO

    def get_synchronized(self, current_user_id: int) -> DataSet:
        return (
            self.model.query.join(DSMetaData)
            .filter(DataSet.user_id == current_user_id, DSMetaData.dataset_doi.isnot(None))
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_unsynchronized(self, current_user_id: int) -> DataSet:
        return (
            self.model.query.join(DSMetaData)
            .filter(DataSet.user_id == current_user_id, DSMetaData.dataset_doi.is_(None))
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_unsynchronized_dataset(self, current_user_id: int, dataset_id: int) -> DataSet:
        return (
            self.model.query.join(DSMetaData)
            .filter(DataSet.user_id == current_user_id, DataSet.id == dataset_id, DSMetaData.dataset_doi.is_(None))
            .first()
        )

    def count_synchronized_datasets(self):
        return (
            self.model.query.join(DSMetaData)
            .filter(DSMetaData.dataset_doi.isnot(None))
            .count()
        )

    def count_unsynchronized_datasets(self):
        return (
            self.model.query.join(DSMetaData)
            .filter(DSMetaData.dataset_doi.is_(None))
            .count()
        )

    def latest_synchronized(self):
        return (
            self.model.query.join(DSMetaData)
            .filter(DSMetaData.dataset_doi.isnot(None))
            .order_by(desc(self.model.id))
            .limit(5)
            .all()
        )

    def get_dataset_with_ratings(self, dataset_id: int):
        dataset = self.model.query.filter_by(id=dataset_id).first()
        if not dataset:
            return None
        average_ratings = self.rating_repository.get_average_rating(dataset_id)
        return {
            "dataset": dataset,
            "ratings": average_ratings
        }


class DOIMappingRepository(BaseRepository):
    def __init__(self):
        super().__init__(DOIMapping)

    def get_new_doi(self, old_doi: str) -> str:
        return self.model.query.filter_by(dataset_doi_old=old_doi).first()


#AÑADIDO
class DatasetRatingRepository(BaseRepository):
    def __init__(self):
        super().__init__(Rating)

    def add_rating(self, dataset_id: int, user_id: int, quality: int, size: int, usability: int) -> Rating:
        total = (quality + size + usability) / 3.0
        new_rating = Rating(
            user_id=user_id,
            dataset_id=dataset_id,
            quality_rating=quality,
            size_rating=size,
            usability_rating=usability,
            total_rating=total,
            created_at=datetime.now(timezone.utc)
        )
        self.db_session.add(new_rating)
        self.db_session.commit()
        logger.info(f"New rating added for dataset {dataset_id} by user {user_id}")
        return new_rating

    def get_average_rating(self, dataset_id: int):
        avg_ratings = self.db_session.query(
            func.avg(Rating.quality_rating).label("average_quality"),
            func.avg(Rating.size_rating).label("average_size"),
            func.avg(Rating.usability_rating).label("average_usability"),
            func.avg(Rating.total_rating).label("average_total")
        ).filter(Rating.dataset_id == dataset_id).one()

        return {
            "average_quality": avg_ratings.average_quality or 0,
            "average_size": avg_ratings.average_size or 0,
            "average_usability": avg_ratings.average_usability or 0,
            "average_total": avg_ratings.average_total or 0
        }
