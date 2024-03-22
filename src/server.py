import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_jwt_extended import get_jwt_identity
from .app.routes import api_blueprint
from src.app.config.extensions import db, ma

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}"
app.config['JWT_SECRET_KEY'] = 'super-secret' 

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario de inicio de sesión
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Verificar si las credenciales son correctas (datos fijos)
    if username == 'admin' and password == '123':
        # Crear el token de acceso
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401

# Ruta protegida que requiere el token de autenticación
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Obtener la identidad del token
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

db.init_app(app)
ma.init_app(app)
app.register_blueprint(api_blueprint)

