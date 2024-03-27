from sqlalchemy import DATE
from marshmallow import fields
from ..config.extensions import ma
from ..models.area import Area


class AreaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Area

    id_area = ma.auto_field()
    nombre =fields.Str()
    clave_contable = fields.Str()
    fecha_registro = fields.Date()
    usuario_registro = fields.Integer()
    activo = fields.Boolean()
    usuario_modifico = fields.Integer()
    fecha_modifico = fields.Date()
