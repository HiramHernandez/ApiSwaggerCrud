from flask_restx import  fields

provider_post_model = {
    'afecta_almacen': fields.Boolean(required=True, description='Si el proveedor tendra almacen'),
    'nombre': fields.String(required=True, description='Nombre del proveedor'),
    'id_grupo_proveedor': fields.Integer(required=True, description='ID del usuario que da de alta el banco'),

    'calle': fields.String(required=True, description='Nombre del proveedor'),
    'numero': fields.String(required=True, description='Nombre del proveedor'),
    'colonia': fields.String(required=True, description='Nombre del proveedor'),
    'ciudad': fields.String(required=True, description='Nombre del proveedor'),
    'estado': fields.String(required=True, description='Nombre del proveedor'),
    'codigo_postal': fields.String(required=True, description='Nombre del proveedor'),
    'correo': fields.String(required=True, description='Nombre del proveedor'),
    'telefono': fields.String(required=True, description='Nombre del proveedor'),
    'rfc': fields.String(required=True, description='Nombre del proveedor'),
    'usuario_registro': fields.Integer(required=True, description='ID del usuario que da de alta el banco'),
    'activo': fields.Boolean(required=True, description='Si el banco estara o no activo')
}

provider_put_model = {
    'afecta_almacen': fields.Boolean(required=True, description='Si el proveedor tendra almacen'),
    'nombre': fields.String(required=True, description='Nombre del proveedor'),
    'id_grupo_proveedor': fields.Integer(required=True, description='ID del usuario que da de alta el banco'),

    'calle': fields.String(required=True, description='Nombre del proveedor'),
    'numero': fields.String(required=True, description='Nombre del proveedor'),
    'colonia': fields.String(required=True, description='Nombre del proveedor'),
    'ciudad': fields.String(required=True, description='Nombre del proveedor'),
    'estado': fields.String(required=True, description='Nombre del proveedor'),
    'codigo_postal': fields.String(required=True, description='Nombre del proveedor'),
    'correo': fields.String(required=True, description='Nombre del proveedor'),
    'telefono': fields.String(required=True, description='Nombre del proveedor'),
    'rfc': fields.String(required=True, description='Nombre del proveedor'),
    'usuario_modifico': fields.Integer(required=True, description='ID del usuario que da de alta el banco'),
    'activo': fields.Boolean(required=True, description='Si el banco estara o no activo')
}

