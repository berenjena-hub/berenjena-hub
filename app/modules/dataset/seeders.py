import os
import shutil
from app.modules.auth.models import User
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics,
    Author)
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import random


class DataSetSeeder(BaseSeeder):

    priority = 2  # Lower priority

    def run(self):
        # Retrieve users
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        # Create DSMetrics instances with varied data
        ds_metrics_list = [
            DSMetrics(
                number_of_models=str(random.randint(3, 10)),
                number_of_features=str(random.randint(20, 100))
            ) for _ in range(3)
        ]
        seeded_ds_metrics = self.seed(ds_metrics_list)

        # Create DSMetaData instances with richer details
        ds_meta_data_list = [
            DSMetaData(
                deposition_id=100 + i,
                title=f'Sample dataset {i+1}',
                description=f'Detailed description for dataset {i+1} with unique insights.',
                publication_type=random.choice(list(PublicationType)),
                publication_doi=f'10.5678/dataset{i+1}',
                dataset_doi=f'10.5678/dataset{i+1}',
                tags=', '.join(random.sample(['analytics', 'AI', 'data', 'research'], 2)),
                ds_metrics_id=random.choice(seeded_ds_metrics).id
            ) for i in range(6)
        ]
        seeded_ds_meta_data = self.seed(ds_meta_data_list)

        # Create varied Author instances and associate with DSMetaData
        authors = [
            Author(
                name=f'Author {i+1}',
                affiliation=f'Institution {random.choice(["A", "B", "C"])}',
                orcid=f'0000-0000-000{i}-000{i+1}',
                ds_meta_data_id=random.choice(seeded_ds_meta_data).id
            ) for i in range(8)
        ]
        self.seed(authors)

        # Create DataSet instances with random creation dates
        datasets = [
            DataSet(
                user_id=random.choice([user1.id, user2.id]),
                ds_meta_data_id=seeded_ds_meta_data[i].id,
                created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 365))
            ) for i in range(6)
        ]
        seeded_datasets = self.seed(datasets)

        # Create more detailed FMMetaData and FeatureModel instances
        fm_meta_data_list = [
            FMMetaData(
                uvl_filename=f'file{i+1}.uvl',
                title=f'Advanced Feature Model {i+1}',
                description=f'In-depth description for feature model {i+1}.',
                publication_type=random.choice(list(PublicationType)),
                publication_doi=f'10.9101/fm{i+1}',
                tags=', '.join(random.sample(['config', 'system', 'modelling'], 2)),
                uvl_version=f'{random.randint(1, 2)}.{random.randint(0, 5)}'
            ) for i in range(12)
        ]
        seeded_fm_meta_data = self.seed(fm_meta_data_list)

        fm_authors = [
            Author(
                name=f'FeatureModel Author {i+1}',
                affiliation=f'Company {random.choice(["X", "Y", "Z"])}',
                orcid=f'0000-0000-000{i+2}-000{i+3}',
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(12)
        ]
        self.seed(fm_authors)

        feature_models = [
            FeatureModel(
                data_set_id=random.choice(seeded_datasets).id,
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(12)
        ]
        seeded_feature_models = self.seed(feature_models)

        # Create and copy files
        load_dotenv()
        working_dir = os.getenv('WORKING_DIR', '')
        src_folder = os.path.join(working_dir, 'app', 'modules', 'dataset', 'uvl_examples')
        for i in range(12):
            file_name = f'file{i+1}.uvl'
            feature_model = seeded_feature_models[i]
            dataset = next(ds for ds in seeded_datasets if ds.id == feature_model.data_set_id)
            user_id = dataset.user_id

            dest_folder = os.path.join(working_dir, 'uploads', f'user_{user_id}', f'dataset_{dataset.id}')
            os.makedirs(dest_folder, exist_ok=True)
            shutil.copy(os.path.join(src_folder, file_name), dest_folder)

            file_path = os.path.join(dest_folder, file_name)

            uvl_file = Hubfile(
                name=file_name,
                checksum=f'checksum{i+1}',
                size=os.path.getsize(file_path),
                feature_model_id=feature_model.id
            )
            self.seed([uvl_file])
