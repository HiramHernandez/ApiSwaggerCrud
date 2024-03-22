from flask_restx import fields

employee_post_model = {
    'nombre': fields.String(required=True, description='Nombre del empleado'),
    'apellido_paterno': fields.String(required=True, description='Apellido paterno del empleado'),
    'apellido_materno': fields.String(required=True, description='Apellido materno del empleado'),
    'calle': fields.String(required=True, description='Calle del empleado'),
    'numero': fields.String(description='Número del empleado'),
    'colonia': fields.String(description='Colonia del empleado'),
    'ciudad': fields.String(description='Ciudad del empleado'),
    'estado': fields.String(description='Estado del empleado'),
    'codigo_postal': fields.Integer(description='Código postal del empleado'),
    'correo': fields.String(description='Correo electrónico del empleado'),
    'telefono': fields.String(description='Teléfono del empleado'),
    'rfc': fields.String(required=True, description='RFC del empleado'),
    'curp': fields.String(required=True, description='CURP del empleado'),
    'imss': fields.String(required=True, description='IMSS del empleado'),
    'tipo_sangre': fields.String(description='Tipo de sangre del empleado'),
    'usuario': fields.String(description='Usuario del empleado'),
    'contrasenia': fields.String(description='Contraseña del empleado'),
    'activo': fields.Boolean(description='Estado de activo del empleado'),
    'usuario_modifico': fields.Integer(description='Usuario que modificó al empleado'),
}

employee_login_model = {
    'usuario': fields.String(description='Usuario del empleado'),
    'contrasenia': fields.String(description='Contraseña del empleado'),
}