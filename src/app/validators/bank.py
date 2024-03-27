from flask_restx import  fields

bank_post_model = {
    'nombre': fields.String(required=True, description='Nombre del banco'),
    'pagina_web': fields.String(required=True, description='Página Web del banco'),
    'usuario_registro': fields.Integer(required=True, description='ID del usuario que da de alta el banco'),
    'activo': fields.Boolean(required=True, description='Si el banco estara o no activo')
}

bank_put_model = {
    'nombre': fields.String(required=True, description='Nombre del banco'),
    'pagina_web': fields.String(required=True, description='Página Web del banco'),
    'usuario_modifico': fields.Integer(required=True, description='ID del usuario que da modifica el banco'),
    'activo': fields.Boolean(required=True, description='Si el banco estara o no activo')
}

