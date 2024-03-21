from sqlalchemy import DATE
from marshmallow import fields
from ..config.extensions import ma
from ..models.employee import Employee


class EmployeeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Employee

    id_empleado = ma.auto_field()
    nombre = ma.auto_field()
    apellido_paterno = ma.auto_field()
    apellido_materno = ma.auto_field()
    calle = ma.auto_field()
    numero = ma.auto_field()
    colonia = ma.auto_field()
    ciudad = ma.auto_field()
    estado = ma.auto_field()
    codigo_postal = ma.auto_field()
    correo = ma.auto_field()
    telefono = ma.auto_field()
    rfc = ma.auto_field()
    curp = ma.auto_field()
    imss = ma.auto_field()
    tipo_sangre = ma.auto_field()
    usuario = ma.auto_field()
    contrasenia = ma.auto_field()
    fecha_registro = fields.Str()
    activo = ma.auto_field()
    fecha_modifico = fields.Str()
