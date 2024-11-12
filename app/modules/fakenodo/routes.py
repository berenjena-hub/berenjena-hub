import uuid
import json
from flask import jsonify, make_response
from app.modules.fakenodo import fakenodo_bp

# obtener todos los datos de `14109910.json`
@fakenodo_bp.route('/fakenodo/deposit/depositions', methods=['GET'])
def get_all():
    with open('app/modules/fakenodo/14109910.json') as f:
        data = json.load(f)
    return jsonify(data)

# crear un nuevo depósito
@fakenodo_bp.route('/fakenodo/deposit/depositions', methods=['POST'])
def create():
    response = make_response(jsonify({"message": "Deposition created", "id": 14109910, "conceptrecid": 14109909}))
    response.status_code = 201
    return response

# subir un archivo al depósito con ID específico
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>/files', methods=['POST'])
def upload(id):
    response = make_response(jsonify({"message": f"File uploaded to deposition {id}"}))
    response.status_code = 201
    return response

# publicar el depósito
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>/actions/publish', methods=['POST'])
def publish(id):
    response = make_response(jsonify({"message": f"Deposition {id} published"}))
    response.status_code = 202
    return response

# eliminar el depósito
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>', methods=['DELETE'])
def delete(id):
    return jsonify({"message": f"Deposition {id} deleted"})

# obtener un depósito específico con DOI aleatorio
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>', methods=['GET'])
def get_deposition(id):
    with open('app/modules/fakenodo/14109910.json') as f:
        data = json.load(f)
        
        # Generar un nuevo DOI único aleatorio para el depósito
        data['pids']['doi']['identifier'] = f"10.5281/zenodo.{uuid.uuid4().int >> 64}"

    return jsonify(data)
