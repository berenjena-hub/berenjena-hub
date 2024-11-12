import uuid
import json
from flask import jsonify, make_response
from app.modules.fakenodo import fakenodo_bp

# Ruta para obtener todos los datos de `14109910.json`
@fakenodo_bp.route('/fakenodo/deposit/depositions', methods=['GET'])
def get_all():
    with open('app/modules/fakenodo/14109910.json') as f:
        data = json.load(f)
    return jsonify(data)

# Ruta para crear un nuevo depósito
@fakenodo_bp.route('/fakenodo/deposit/depositions', methods=['POST'])
def create():
    response = make_response(jsonify({"message": "Deposition created", "id": 14109910, "conceptrecid": 14109909}))
    response.status_code = 201
    return response

# Ruta para subir un archivo al depósito con ID específico
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>/files', methods=['POST'])
def upload(id):
    response = make_response(jsonify({"message": f"File uploaded to deposition {id}"}))
    response.status_code = 201
    return response

# Ruta para "publicar" el depósito
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>/actions/publish', methods=['POST'])
def publish(id):
    response = make_response(jsonify({"message": f"Deposition {id} published"}))
    response.status_code = 202
    return response

# Ruta para eliminar el depósito
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>', methods=['DELETE'])
def delete(id):
    return jsonify({"message": f"Deposition {id} deleted"})

# Ruta para obtener un depósito específico con DOI aleatorio
@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>', methods=['GET'])
def get_deposition(id):
    with open('app/modules/fakenodo/14109910.json') as f:
        data = json.load(f)
        
        # Generar un nuevo DOI único aleatorio para el depósito
        data['pids']['doi']['identifier'] = f"10.5281/zenodo.{uuid.uuid4().int >> 64}"

    return jsonify(data)
