from flask_restx import  fields

device_post_model = {
    'nombre': fields.String(required=True, description='Nombre del dispositivo'),
    'tipo_dispositivo_id': fields.Integer(required=True, description='ID del tipo de dispositivo'),
    'estatus_dispositivo_id': fields.Integer(required=True, description='ID del estatus del dispositivo'),
    'potencia': fields.Integer(required=True, description='Potencia del dispositivo')
}
