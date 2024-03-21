from sqlalchemy import Column, Integer, VARCHAR, DATE, BOOLEAN
from ..config.extensions import db


class Employee(db.Model):
    __tablename__ = 'cat_empleados'
    __table_args__ = {'implicit_returning': False}

    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(VARCHAR(length=50))
    apellido_paterno = Column(VARCHAR(length=50))
    apellido_materno = Column(VARCHAR(length=50))
    calle = Column(VARCHAR(length=100), nullable=False)
    numero = Column(VARCHAR(length=50))
    colonia = Column(VARCHAR(length=50))
    ciudad = Column(VARCHAR(length=30))
    estado = Column(VARCHAR(length=30))
    codigo_postal = Column(Integer)
    correo = Column(VARCHAR(length=50))
    telefono = Column(VARCHAR(length=20))
    rfc = Column(VARCHAR(length=20), nullable=False)
    curp = Column(VARCHAR(length=30), nullable=False)
    imss = Column(VARCHAR(length=20), nullable=False)
    tipo_sangre = Column(VARCHAR(length=30))
    usuario = Column(VARCHAR(length=50))
    contrasenia = Column(VARCHAR(length=10))
    fecha_registro = Column(DATE)
    activo = Column(BOOLEAN, nullable=False, default=1)
    usuario_modifico = Column(Integer)
    fecha_modifico = Column(DATE)
