from datetime import datetime, timezone
import os
import uuid
import requests
from flask import current_app, jsonify, make_response, request, send_from_directory
from flask_login import current_user
from app.modules.hubfile import hubfile_bp
from app.modules.hubfile.models import HubfileDownloadRecord, HubfileViewRecord
from app.modules.hubfile.services import HubfileDownloadRecordService, HubfileService
from bs4 import BeautifulSoup

from app import db


@hubfile_bp.route("/file/download/<int:file_id>", methods=["GET"])
def download_file(file_id):
    file = HubfileService().get_or_404(file_id)
    filename = file.name

    directory_path = f"uploads/user_{file.feature_model.data_set.user_id}/dataset_{file.feature_model.data_set_id}/"
    parent_directory_path = os.path.dirname(current_app.root_path)
    file_path = os.path.join(parent_directory_path, directory_path, filename)

    # URL pública en GitHub
    github_raw_url = f"https://raw.githubusercontent.com/berenjena-hub/files/main/uploads/user_{file.feature_model.data_set.user_id}/dataset_{file.feature_model.data_set_id}/{filename}"

    # Get or generate a cookie for the download
    user_cookie = request.cookies.get("file_download_cookie")
    if not user_cookie:
        user_cookie = str(uuid.uuid4())

    # Check for existing download record
    existing_record = HubfileDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        file_id=file_id,
        download_cookie=user_cookie
    ).first()

    if not existing_record:
        # Record the download in the database
        HubfileDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            file_id=file_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    # Check if file exists locally; if not, fetch it from GitHub
    if not os.path.isfile(file_path):
        try:
            response = requests.get(github_raw_url, stream=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
            else:
                return jsonify({"error": "Failed to download file from GitHub"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Send the file as a response
    resp = make_response(
        send_from_directory(directory=os.path.dirname(file_path), path=filename, as_attachment=True)
    )
    resp.set_cookie("file_download_cookie", user_cookie)

    return resp


@hubfile_bp.route('/file/view/<int:file_id>', methods=['GET'])
def view_file(file_id):
    # Obtener el archivo desde la base de datos
    file = HubfileService().get_or_404(file_id)
    filename = file.name

    # Ruta local
    directory_path = f"uploads/user_{file.feature_model.data_set.user_id}/dataset_{file.feature_model.data_set_id}/"
    parent_directory_path = os.path.dirname(current_app.root_path)
    file_path = os.path.join(parent_directory_path, directory_path, filename)

    # URL Raw de GitHub
    github_raw_url = f"https://raw.githubusercontent.com/berenjena-hub/files/main/uploads/user_{file.feature_model.data_set.user_id}/dataset_{file.feature_model.data_set_id}/{filename}"

    try:
        # Intentar leer desde el archivo local
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
        else:
            # Si no está localmente, intentar obtener desde GitHub Raw
            response = requests.get(github_raw_url)
            if response.status_code != 200:
                return jsonify({'success': False, 'error': 'GitHub Raw file not accessible'}), 404

            # Si tiene éxito, usar el contenido del Raw
            content = response.text

        # Registro de vistas (cookie y base de datos)
        user_cookie = request.cookies.get('view_cookie', str(uuid.uuid4()))
        existing_record = HubfileViewRecord.query.filter_by(
            user_id=current_user.id if current_user.is_authenticated else None,
            file_id=file_id,
            view_cookie=user_cookie
        ).first()

        if not existing_record:
            new_view_record = HubfileViewRecord(
                user_id=current_user.id if current_user.is_authenticated else None,
                file_id=file_id,
                view_date=datetime.now(),
                view_cookie=user_cookie
            )
            db.session.add(new_view_record)
            db.session.commit()

        # Preparar la respuesta
        response = jsonify({'success': True, 'content': content})
        if not request.cookies.get('view_cookie'):
            response = make_response(response)
            response.set_cookie('view_cookie', user_cookie, max_age=60 * 60 * 24 * 365 * 2)

        return response

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
