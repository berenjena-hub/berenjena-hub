import logging
import os
import json
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from zipfile import ZipFile

from flask import (
    redirect,
    render_template,
    request,
    jsonify,
    send_from_directory,
    make_response,
    abort,
    url_for,
)
from flask_login import login_required, current_user


from app.modules.dataset.forms import DataSetForm
from app.modules.dataset.models import (
    DSDownloadRecord, 
    Rating
)
from app.modules.dataset import dataset_bp
from app.modules.dataset.services import (
    AuthorService,
    DSDownloadRecordService,
    DSMetaDataService,
    DSViewRecordService,
    DataSetService,
    DOIMappingService, 
    RatingService
)
from app.modules.zenodo.services import ZenodoService
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, GlencoeWriter, SPLOTWriter, JSONWriter, AFMWriter
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat, DimacsWriter
from app.modules.hubfile.services import HubfileService

from sqlalchemy.orm import Session
from app import db 

logger = logging.getLogger(__name__)


dataset_service = DataSetService()
author_service = AuthorService()
dsmetadata_service = DSMetaDataService()
zenodo_service = ZenodoService()
doi_mapping_service = DOIMappingService()
ds_view_record_service = DSViewRecordService()
#AÑADIDO
rating_service = RatingService()


@dataset_bp.route("/dataset/upload", methods=["GET", "POST"])
@login_required
def create_dataset():
    form = DataSetForm()
    if request.method == "POST":

        dataset = None

        if not form.validate_on_submit():
            return jsonify({"message": form.errors}), 400

        try:
            logger.info("Creating dataset...")
            dataset = dataset_service.create_from_form(form=form, current_user=current_user)
            logger.info(f"Created dataset: {dataset}")
            dataset_service.move_feature_models(dataset)
        except Exception as exc:
            logger.exception(f"Exception while create dataset data in local {exc}")
            return jsonify({"Exception while create dataset data in local: ": str(exc)}), 400

        # send dataset as deposition to Zenodo
        data = {}
        try:
            zenodo_response_json = zenodo_service.create_new_deposition(dataset)
            response_data = json.dumps(zenodo_response_json)
            data = json.loads(response_data)
        except Exception as exc:
            data = {}
            zenodo_response_json = {}
            logger.exception(f"Exception while create dataset data in Zenodo {exc}")

        if data.get("conceptrecid"):
            deposition_id = data.get("id")

            # update dataset with deposition id in Zenodo
            dataset_service.update_dsmetadata(dataset.ds_meta_data_id, deposition_id=deposition_id)

            try:
                # iterate for each feature model (one feature model = one request to Zenodo)
                for feature_model in dataset.feature_models:
                    zenodo_service.upload_file(dataset, deposition_id, feature_model)

                # publish deposition
                zenodo_service.publish_deposition(deposition_id)

                # update DOI
                deposition_doi = zenodo_service.get_doi(deposition_id)
                dataset_service.update_dsmetadata(dataset.ds_meta_data_id, dataset_doi=deposition_doi)
            except Exception as e:
                msg = f"it has not been possible upload feature models in Zenodo and update the DOI: {e}"
                return jsonify({"message": msg}), 200

        # Delete temp folder
        file_path = current_user.temp_folder()
        if os.path.exists(file_path) and os.path.isdir(file_path):
            shutil.rmtree(file_path)

        msg = "Everything works!"
        return jsonify({"message": msg}), 200

    return render_template("dataset/upload_dataset.html", form=form)


@dataset_bp.route("/dataset/list", methods=["GET", "POST"])
@login_required
def list_dataset():
    return render_template(
        "dataset/list_datasets.html",
        datasets=dataset_service.get_synchronized(current_user.id),
        local_datasets=dataset_service.get_unsynchronized(current_user.id),
    )


@dataset_bp.route("/dataset/file/upload", methods=["POST"])
@login_required
def upload():
    file = request.files["file"]
    temp_folder = current_user.temp_folder()

    if not file or not file.filename.endswith(".uvl"):
        return jsonify({"message": "No valid file"}), 400

    # create temp folder
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    file_path = os.path.join(temp_folder, file.filename)

    if os.path.exists(file_path):
        # Generate unique filename (by recursion)
        base_name, extension = os.path.splitext(file.filename)
        i = 1
        while os.path.exists(
            os.path.join(temp_folder, f"{base_name} ({i}){extension}")
        ):
            i += 1
        new_filename = f"{base_name} ({i}){extension}"
        file_path = os.path.join(temp_folder, new_filename)
    else:
        new_filename = file.filename

    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    return (
        jsonify(
            {
                "message": "UVL uploaded and validated successfully",
                "filename": new_filename,
            }
        ),
        200,
    )


@dataset_bp.route("/dataset/file/delete", methods=["POST"])
def delete():
    data = request.get_json()
    filename = data.get("file")
    temp_folder = current_user.temp_folder()
    filepath = os.path.join(temp_folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": "File deleted successfully"})

    return jsonify({"error": "Error: File not found"})


@dataset_bp.route("/dataset/download/<int:dataset_id>", methods=["GET"])
def download_dataset(dataset_id):
    dataset = dataset_service.get_or_404(dataset_id)

    file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"dataset_{dataset_id}.zip")

    with ZipFile(zip_path, "w") as zipf:
        for subdir, dirs, files in os.walk(file_path):
            for file in files:
                full_path = os.path.join(subdir, file)

                relative_path = os.path.relpath(full_path, file_path)

                zipf.write(
                    full_path,
                    arcname=os.path.join(
                        os.path.basename(zip_path[:-4]), relative_path
                    ),
                )

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(
            uuid.uuid4()
        )  # Generate a new unique identifier if it does not exist
        # Save the cookie to the user's browser
        resp = make_response(
            send_from_directory(
                temp_dir,
                f"dataset_{dataset_id}.zip",
                as_attachment=True,
                mimetype="application/zip",
            )
        )
        resp.set_cookie("download_cookie", user_cookie)
    else:
        resp = send_from_directory(
            temp_dir,
            f"dataset_{dataset_id}.zip",
            as_attachment=True,
            mimetype="application/zip",
        )

    # Check if the download record already exists for this cookie
    existing_record = DSDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        dataset_id=dataset_id,
        download_cookie=user_cookie
    ).first()

    if not existing_record:
        # Record the download in your database
        DSDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    return resp


@dataset_bp.route("/dataset/download/<int:dataset_id>/<string:format>", methods=["GET"])
def download_dataset_format(dataset_id, format):
    dataset = dataset_service.get_or_404(dataset_id)
    file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"dataset_{dataset_id}.zip")

    with ZipFile(zip_path, "w") as zipf:
        for subdir, dirs, files in os.walk(file_path):
            for file in dataset.files():
                full_path = os.path.join(subdir, file.name)
                with open(full_path, "r") as file_content:
                    content = file_content.read()
                name = f"{file.name}"
                if format == "glencoe":
                    hubfile = HubfileService().get_or_404(file.id)
                    temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                    fm = UVLReader(hubfile.get_path()).transform()
                    GlencoeWriter(temp_file.name, fm).transform()
                    with open(temp_file.name, "r") as new_format_file:
                        content = new_format_file.read()
                    name = f"{hubfile.name}_glencoe.txt"
                elif format == "dimacs":
                    temp_file = tempfile.NamedTemporaryFile(suffix='.cnf', delete=False)
                    hubfile = HubfileService().get_by_id(file.id)
                    fm = UVLReader(hubfile.get_path()).transform()
                    sat = FmToPysat(fm).transform()
                    DimacsWriter(temp_file.name, sat).transform()
                    with open(temp_file.name, "r") as new_format_file:
                        content = new_format_file.read()
                    name = f"{hubfile.name}_cnf.txt"
                elif format == "splot":
                    hubfile = HubfileService().get_by_id(file.id)
                    temp_file = tempfile.NamedTemporaryFile(suffix='.splx', delete=False)
                    fm = UVLReader(hubfile.get_path()).transform()
                    SPLOTWriter(temp_file.name, fm).transform()
                    with open(temp_file.name, "r") as new_format_file:
                        content = new_format_file.read()
                    name = f"{hubfile.name}_splot.txt"
                elif format == "json":
                    temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                    hubfile = HubfileService().get_by_id(file.id)
                    fm = UVLReader(hubfile.get_path()).transform()
                    JSONWriter(temp_file.name, fm).transform()
                    with open(temp_file.name, "r") as new_format_file:
                        content = new_format_file.read()
                    name = f"{hubfile.name}_json.txt"
                elif format == "afm":
                    temp_file = tempfile.NamedTemporaryFile(suffix='.afm', delete=False)
                    hubfile = HubfileService().get_by_id(file.id)
                    fm = UVLReader(hubfile.get_path()).transform()
                    AFMWriter(temp_file.name, fm).transform()
                    with open(temp_file.name, "r") as new_format_file:
                        content = new_format_file.read()
                    name = f"{hubfile.name}_afm.txt"
                with zipf.open(name, "w") as zipfile:
                    zipfile.write(content.encode())

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(
            uuid.uuid4()
        )  # Generate a new unique identifier if it does not exist
        # Save the cookie to the user's browser
        resp = make_response(
            send_from_directory(
                temp_dir,
                f"dataset_{dataset_id}.zip",
                as_attachment=True,
                mimetype="application/zip",
            )
        )
        resp.set_cookie("download_cookie", user_cookie)
    else:
        resp = send_from_directory(
            temp_dir,
            f"dataset_{dataset_id}.zip",
            as_attachment=True,
            mimetype="application/zip",
        )

    # Check if the download record already exists for this cookie
    existing_record = DSDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        dataset_id=dataset_id,
        download_cookie=user_cookie
    ).first()

    if not existing_record:
        # Record the download in your database
        DSDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    return resp


@dataset_bp.route("/doi/<path:doi>/", methods=["GET"])
def subdomain_index(doi):

    # Check if the DOI is an old DOI
    new_doi = doi_mapping_service.get_new_doi(doi)
    if new_doi:
        # Redirect to the same path with the new DOI
        return redirect(url_for('dataset.subdomain_index', doi=new_doi), code=302)

    # Try to search the dataset by the provided DOI (which should already be the new one)
    ds_meta_data = dsmetadata_service.filter_by_doi(doi)

    if not ds_meta_data:
        abort(404)

    # Get dataset
    dataset = ds_meta_data.data_set

    # Save the cookie to the user's browser
    user_cookie = ds_view_record_service.create_cookie(dataset=dataset)
    resp = make_response(render_template("dataset/view_dataset.html", dataset=dataset))
    resp.set_cookie("view_cookie", user_cookie)

    return resp


@dataset_bp.route("/dataset/unsynchronized/<int:dataset_id>/", methods=["GET"])
@login_required
def get_unsynchronized_dataset(dataset_id):

    # Get dataset
    dataset = dataset_service.get_unsynchronized_dataset(current_user.id, dataset_id)

    if not dataset:
        abort(404)

    return render_template("dataset/view_dataset.html", dataset=dataset)

#AÑADIDO
@dataset_bp.route("/rate", methods=["POST"])
@login_required
def rate():
    user_id = request.json.get("user_id")
    dataset_id = request.json.get("dataset_id")
    quality = request.json.get("quality")
    size = request.json.get("size")
    usability = request.json.get("usability")

    if not all([user_id, dataset_id, quality, size, usability]):
        return jsonify({"message": "Faltan parámetros en la solicitud"}), 400

    try:
        quality = float(quality)
        size = float(size)
        usability = float(usability)

        if not all(1 <= x <= 5 for x in [quality, size, usability]):
            return jsonify({"message": "Las calificaciones deben estar entre 1 y 5"}), 400
        
        existing_rating = db.session.query(Rating).filter_by(user_id=user_id, dataset_id=dataset_id).first()
        if existing_rating:
            existing_rating.quality = quality
            existing_rating.size = size
            existing_rating.usability = usability
            existing_rating.total_rating = (quality + size + usability) / 3
        else:
            rating = Rating(
                user_id=user_id,
                dataset_id=dataset_id,
                quality=quality,
                size=size,
                usability=usability,
                total_rating=(quality + size + usability) / 3
            )
            db.session.add(rating)

        db.session.commit()

        avg_ratings = rating_service.get_average_rating(dataset_id)
        avg_ratings = {key: float(value) for key, value in avg_ratings.items()}

        return jsonify({
            "message": "Calificación guardada correctamente",
            "avg_ratings": avg_ratings
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Error de tipo: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        logger.exception("Error al agregar la calificación")
        return jsonify({"error": str(e)}), 400


@dataset_bp.route('/ratings/<int:dataset_id>', methods=['GET'])
def get_ratings(dataset_id):
    try:
        avg_ratings = db.session.query(
            db.func.coalesce(db.func.avg(Rating.quality), 0).label('average_quality'),
            db.func.coalesce(db.func.avg(Rating.size), 0).label('average_size'),
            db.func.coalesce(db.func.avg(Rating.usability), 0).label('average_usability'),
            db.func.coalesce(db.func.avg(Rating.total_rating), 0).label('average_total')
        ).filter_by(dataset_id=dataset_id).first()

        user_id = request.args.get('user_id') 
        user_rating = None
        if user_id:
            user_rating = Rating.query.filter_by(dataset_id=dataset_id, user_id=user_id).first()

        return jsonify({
            "avg_ratings": {
                "quality": avg_ratings.average_quality or 0,
                "size": avg_ratings.average_size or 0,
                "usability": avg_ratings.average_usability or 0,
                "total": avg_ratings.average_total or 0,
            },
            "user_rating": {
                "quality": user_rating.quality if user_rating else None,
                "size": user_rating.size if user_rating else None,
                "usability": user_rating.usability if user_rating else None,
            } if user_rating else None
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@dataset_bp.route("/doi/<doi>", methods=["GET"])
def view_dataset(doi):
    dataset_id = get_dataset_id(doi)
    user_id = current_user.id if current_user.is_authenticated else None
    if not dataset_id:
        abort(404) 

    avg_ratings = rating_service.get_average_rating(dataset_id)

    return render_template(
        "dataset/view_dataset.html",
        dataset_id=dataset_id,
        user_id=user_id,
        avg_quality=avg_ratings.get("quality", 0),
        avg_size=avg_ratings.get("size", 0),
        avg_usability=avg_ratings.get("usability", 0)
    )


@dataset_bp.route("/file_content/<int:dataset_id>/<int:file_id>/", methods=["GET"])
def get_file_content(file_id, dataset_id):
    return render_template("dataset/file_content.html", file_id=file_id, 
                           dataset=dataset_service.get_or_404(dataset_id))

