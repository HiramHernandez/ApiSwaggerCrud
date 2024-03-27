from sqlalchemy import Column, Integer, VARCHAR, DATE, BOOLEAN

from ..config.extensions import db


class CatBanco(db.Model):
    __tablename__ = 'cat_bancos'

    id_banco = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(VARCHAR(length=80), nullable=False)
    pagina_web = Column(VARCHAR(length=50), nullable=False)
    fecha_registro = Column(DATE, nullable=False)
    usuario_registro = Column(Integer, default=None)
    activo = Column(BOOLEAN, nullable=False, default=1)
    usuario_modifico = Column(Integer, default=None)
    fecha_modifico = Column(DATE, default=None)
