import logging
from datetime import datetime
from sqlalchemy.sql import func
from ..config.extensions import db
from ..models.provider import Provider


class ProviderService:
    _instance = None
    _logger = logging.getLogger(__name__)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    # se retorna data -> objeto, error -> booleano
    def fetch_all(self, page=1, size=20):
        try:
            providers = db.session.query(Provider).paginate(int(page), size)
            return (providers, False)
        except Exception as e:
            self._logger.error(f"Error al obtener todos los proveedores: {e}", exc_info=True)
            return ([], True)
    
    def fetch_by_id(self, id):
        try:
            provider = db.session.query(Provider).filter(Provider.id_proveedor == id).first()
            return (provider, False)
        except Exception as e:
            self._logger.error(f"Error al obtener el proveedor con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def create(self, data):
        try:
            new_provider = Provider(
                afecta_almacen = data['afecta_almacen'],
                nombre = data['nombre'],
                id_grupo_proveedor = data['id_grupo_proveedor'],
                calle = data['calle'],
                numero = data['numero'],
                colonia = data['colonia'],
                ciudad = data['ciudad'],
                estado = data['estado'],
                codigo_postal  = data['codigo_postal'],
                correo = data['correo'],
                telefono = data['telefono'],
                rfc = data['rfc'],
                fecha_registro = datetime.now(),
                usuario_registro = data['usuario_registro'],
                activo = True
            )
            db.session.add(new_provider)
            db.session.commit()
            return (new_provider, False)
        except Exception as e:
            self._logger.error(f"Error al crear el proveedor: {e}", exc_info=True)
            return (None, True)
        
    def update(self, id, data):
        try:
            provider = db.session.query(Provider).filter(Provider.id_proveedor == id).first()
            if not provider:
                return (None, False)
            for key, value in data.items():
                setattr(provider, key, value)
            provider.fecha_modifico = datetime.now()
            db.session.commit()
            return (provider, False)
        except Exception as e:
            self._logger.error(f"Error al actualizar el proveedor con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def delete(self, id):
        try:
            provider = db.session.query(Provider).filter(Provider.id_proveedor == id).first()
            if not provider:
                return False
            db.session.delete(provider)
            db.session.commit()
            return True
            
        except Exception as e:
            self._logger.error(f"Error al eliminar el proveedor con ID {id}: {e}", exc_info=True)
            return False
