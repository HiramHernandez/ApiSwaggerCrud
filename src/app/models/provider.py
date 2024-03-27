from sqlalchemy import Column, Integer, VARCHAR, DATE, BOOLEAN
from ..config.extensions import db


class Provider(db.Model):
    __tablename__ = 'cat_proveedores'

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    afecta_almacen = Column(BOOLEAN, nullable=False, default=1)
    nombre = Column(VARCHAR(length=80), nullable=False)
    id_grupo_proveedor = Column(Integer, nullable=False)
    calle = Column(VARCHAR(length=50), nullable=False)
    numero = Column(VARCHAR(length=50), nullable=False)
    colonia = Column(VARCHAR(length=50), nullable=False)
    ciudad = Column(VARCHAR(length=50), nullable=False)
    estado = Column(VARCHAR(length=50), nullable=False)
    codigo_postal  = Column(VARCHAR(length=50), nullable=False)
    correo = Column(VARCHAR(length=50), nullable=False)
    telefono = Column(VARCHAR(length=50), nullable=False)
    rfc = Column(VARCHAR(length=50), nullable=False)
    fecha_registro = Column(DATE, nullable=False)
    usuario_registro = Column(Integer, default=None)
    activo = Column(BOOLEAN, nullable=False, default=1)
    usuario_modifico = Column(Integer, default=None)
    fecha_modifico = Column(DATE, default=None)
