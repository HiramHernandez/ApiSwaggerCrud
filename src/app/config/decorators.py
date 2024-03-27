from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Falta el token de autorización'}), 401

        parts = auth_header.split()
        if parts[0] != 'Bearer':
            return jsonify({'message': 'Token de autorización inválido'}), 401

        token = parts[1]

        # Validar el token (por ejemplo, con una API de autenticación)

        if not is_valid_token(token):
            return jsonify({'message': 'Token de autorización inválido'}), 401

        return f(*args, **kwargs)

    return decorated