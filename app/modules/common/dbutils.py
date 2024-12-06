import os
import shutil
from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics)
from app.modules.hubfile.models import Hubfile
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from datetime import datetime, timezone
from dotenv import load_dotenv


def create_dataset_db(id, publication_type=PublicationType.DATA_MANAGEMENT_PLAN, tags=""):
    user_test = User(email=f'user{id}@example.com', password='test1234')
    db.session.add(user_test)
    db.session.commit()

    ds_metrics = DSMetrics(number_of_models='1', number_of_features='5')
    db.session.add(ds_metrics)
    db.session.commit()

    ds_meta_data = DSMetaData(
            deposition_id=id,
            title=f'Sample dataset {id}',
            description=f'Description for dataset {id}',
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi=f'10.1234/dataset{id}',
            dataset_doi=f'10.1234/dataset{id}',
            tags='tag1, tag2',
            ds_metrics_id=ds_metrics.id
        )
    db.session.add(ds_meta_data)
    db.session.commit()

    dataset = DataSet(
            user_id=user_test.id,
            ds_meta_data_id=ds_meta_data.id,
            created_at=datetime.now(timezone.utc)
        )
    db.session.add(dataset)
    db.session.commit()

    fm_meta_data = FMMetaData(
            uvl_filename=f'file{id}.uvl',
            title=f'Feature Model {id}',
            description=f'Description for feature model {id}',
            publication_type=PublicationType.SOFTWARE_DOCUMENTATION,
            publication_doi='10.1234/fm1',
            tags=tags,
            uvl_version='1.0'
        )
    db.session.add(fm_meta_data)
    db.session.commit()

    feature_model = FeatureModel(
            data_set_id=dataset.id,
            fm_meta_data_id=fm_meta_data.id
        )
    db.session.add(feature_model)
    db.session.commit()

    load_dotenv()
    working_dir = os.getenv('WORKING_DIR', '')
    file_name = f'file{id}.uvl'
    src_folder = os.path.join(working_dir, 'app', 'modules', 'dataset', 'uvl_examples')

    dest_folder = os.path.join(working_dir, 'uploads', f'user_{user_test.id}', f'dataset_{dataset.id}')
    os.makedirs(dest_folder, exist_ok=True)
    shutil.copy(os.path.join(src_folder, file_name), dest_folder)

    file_path = os.path.join(dest_folder, file_name)

    uvl_file = Hubfile(
        name=file_name,
        checksum=f'checksum{id}',
        size=os.path.getsize(file_path),
        feature_model_id=feature_model.id
    )
    db.session.add(uvl_file)
    db.session.commit()
