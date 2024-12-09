import pytest
import os
import shutil
from app import db
from app.modules.flamapy.routes import to_glencoe, to_splot, to_cnf, to_json, to_afm
from app.modules.auth.models import User
from app.modules.featuremodel.models import FeatureModel
from app.modules.hubfile.models import Hubfile
from app.modules.dataset.models import DSMetaData, PublicationType, DataSet


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        user = create_user(email="test_user@example.com", password="test1234")
        dataset = create_dataset(user_id=user.id)
        os.makedirs(f"uploads/user_{user.id}/dataset_{dataset.id}", exist_ok=True)
        with open(f"uploads/user_{user.id}/dataset_{dataset.id}/filetest.uvl", "w") as f:
            f.write('features\n    Chat\n        mandatory\n            Connection\n                alternative\n                    "Peer 2 Peer"\n                    Server\n            Messages\n                or\n                    Text\n                    Video\n                    Audio\n        optional\n            "Data Storage"\n            "Media Player"\n\nconstraints\n    Server => "Data Storage"\n    Video | Audio => "Media Player"\n')
    yield test_client
    with test_client.application.app_context():
        db.session.delete(dataset)
        db.session.delete(user)
        db.session.commit()
        shutil.rmtree(f"uploads/user_{user.id}/dataset_{dataset.id}", ignore_errors=True)


def create_user(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def create_dataset(user_id):
    ds_meta_data = DSMetaData(title="Test Dataset", description="Test dataset description", publication_type=PublicationType.JOURNAL_ARTICLE)
    db.session.add(ds_meta_data)
    db.session.commit()
    dataset = DataSet(user_id=user_id, ds_meta_data_id=ds_meta_data.id)
    db.session.add(dataset)
    db.session.commit()
    return dataset


def create_feature_model(dataset_id):
    feature_model = FeatureModel(data_set_id=dataset_id)
    db.session.add(feature_model)
    db.session.commit()
    return feature_model


def create_hubfile(name, feature_model_id, user_id, dataset_id):
    file_path = f"uploads/user_{user_id}/dataset_{dataset_id}/{name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(
            "features\n"
            "    Chat\n"
            "        mandatory\n"
            "            Connection\n"
            "                alternative\n"
            '                    "Peer 2 Peer"\n'
            "                    Server\n"
            "            Messages\n"
            "                or\n"
            "                    Text\n"
            "                    Video\n"
            "                    Audio\n"
            "        optional\n"
            '            "Data Storage"\n'
            '            "Media Player"\n'
            "\n"
            "constraints\n"
            '    Server => "Data Storage"\n'
            '    Video | Audio => "Media Player"\n'
        )
    hubfile = Hubfile(name=name, checksum="123456", size=100, feature_model_id=feature_model_id)
    db.session.add(hubfile)
    db.session.commit()
    return hubfile


def delete_folder(user, dataset):
    if user.id != 2 or user.id != 1:
        shutil.rmtree(f"uploads/user_{user.id}", ignore_errors=True)
    else:
        shutil.rmtree(f"uploads/user_{user.id}/dataset_{dataset.id}", ignore_errors=True)


def test_to_glencoe(test_client):
    user = create_user(email="test_user_glencoe@example.com", password="test1234")
    dataset = create_dataset(user_id=user.id)
    fm = create_feature_model(dataset_id=dataset.id)
    hubfile = create_hubfile(name="test_hubfile", feature_model_id=fm.id, user_id=user.id, dataset_id=dataset.id)
    os.environ["WORKING_DIR"] = os.getcwd()
    with test_client.application.test_request_context():
        response = to_glencoe(file_id=hubfile.id)
        assert response.status_code == 200, "No se realizó la descarga correctamente"
        content_disposition = response.headers.get("Content-Disposition")
        assert "test_hubfile_glencoe.txt" in content_disposition, "El formato no es correcto"
    db.session.delete(hubfile)
    db.session.delete(dataset)
    db.session.delete(user)
    db.session.commit()
    delete_folder(user, dataset)


def test_to_splot(test_client):
    user = create_user(email="test_user_splot@example.com", password="test1234")
    dataset = create_dataset(user_id=user.id)
    fm = create_feature_model(dataset_id=dataset.id)
    hubfile = create_hubfile(name="test_hubfile", feature_model_id=fm.id, user_id=user.id, dataset_id=dataset.id)
    os.environ["WORKING_DIR"] = os.getcwd()
    with test_client.application.test_request_context():
        response = to_splot(file_id=hubfile.id)
        assert response.status_code == 200, "No se realizó la descarga correctamente"
        content_disposition = response.headers.get("Content-Disposition")
        assert "test_hubfile_splot.txt" in content_disposition, "El formato no es correcto"
    db.session.delete(hubfile)
    db.session.delete(dataset)
    db.session.delete(user)
    db.session.commit()
    delete_folder(user, dataset)


def test_to_cnf(test_client):
    user = create_user(email="test_user_cnf@example.com", password="test1234")
    dataset = create_dataset(user_id=user.id)
    fm = create_feature_model(dataset_id=dataset.id)
    hubfile = create_hubfile(name="test_hubfile", feature_model_id=fm.id, user_id=user.id, dataset_id=dataset.id)
    os.environ["WORKING_DIR"] = os.getcwd()
    with test_client.application.test_request_context():
        response = to_cnf(file_id=hubfile.id)
        assert response.status_code == 200, "No se realizó la descarga correctamente"
        content_disposition = response.headers.get("Content-Disposition")
        assert "test_hubfile_cnf.txt" in content_disposition, "El formato no es correcto"
    db.session.delete(hubfile)
    db.session.delete(dataset)
    db.session.delete(user)
    db.session.commit()
    delete_folder(user, dataset)


def test_to_json(test_client):
    user = create_user(email="test_user_json@example.com", password="test1234")
    dataset = create_dataset(user_id=user.id)
    fm = create_feature_model(dataset_id=dataset.id)
    hubfile = create_hubfile(name="test_hubfile", feature_model_id=fm.id, user_id=user.id, dataset_id=dataset.id)
    os.environ["WORKING_DIR"] = os.getcwd()
    with test_client.application.test_request_context():
        response = to_json(file_id=hubfile.id)
        assert response.status_code == 200, "No se realizó la descarga correctamente"
        content_disposition = response.headers.get("Content-Disposition")
        assert "test_hubfile_json.txt" in content_disposition, "El formato no es correcto"
    db.session.delete(hubfile)
    db.session.delete(dataset)
    db.session.delete(user)
    db.session.commit()
    delete_folder(user, dataset)
