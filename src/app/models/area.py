from sqlalchemy import Column, Integer, VARCHAR, DATE, BOOLEAN

from ..config.extensions import db


class Area(db.Model):
    __tablename__ = 'cat_areas'

    id_area = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(VARCHAR(length=50), nullable=False)
    clave_contable = Column(VARCHAR(length=4), nullable=False)
    fecha_registro = Column(DATE, nullable=False)
    usuario_registro = Column(Integer, nullable=False)
    activo = Column(BOOLEAN, nullable=False, default=1)
    usuario_modifico = Column(Integer, default=None)
    fecha_modifico = Column(DATE, default=None)
