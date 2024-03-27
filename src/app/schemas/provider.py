from sqlalchemy import DATE
from marshmallow import fields
from ..config.extensions import ma
from ..models.provider import Provider


class ProviderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Provider

    id_proveedor = ma.auto_field()
    afecta_almacen = fields.Boolean()
    nombre = fields.String()
    id_grupo_proveedor = fields.Integer()
    calle = fields.String()
    numero = fields.String()
    colonia = fields.String()
    ciudad = fields.String()
    estado = fields.String()
    codigo_postal  = fields.String()
    correo = fields.String()
    telefono = fields.String()
    rfc = fields.String()
    fecha_registro = fields.Date()
    usuario_registro = fields.Integer()
    activo = fields.Boolean()
    usuario_modifico = fields.Integer()
    fecha_modifico = fields.Date()
