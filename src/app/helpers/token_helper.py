from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_jwt_extended import get_jwt_identity
from ..models.employee import Employee

def create_token(employee: Employee):
    return create_access_token(identity=employee.id_empleado)