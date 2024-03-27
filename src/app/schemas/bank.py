from sqlalchemy import DATE
from marshmallow import fields
from ..config.extensions import ma
from ..models.bank import Bank


class BankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bank

    id_banco = ma.auto_field()
    nombre = fields.Str()
    pagina_web = fields.Str()
    fecha_registro = fields.Date()
    usuario_registro = fields.Integer()
    activo = fields.Boolean()
    usuario_modifico = fields.Integer()
    fecha_modifico = fields.Date()

