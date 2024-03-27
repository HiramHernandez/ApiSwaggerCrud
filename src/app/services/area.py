import logging
from datetime import datetime
from sqlalchemy.sql import func
from ..config.extensions import db
from ..models.area import Area


class AreaService:
    _instance = None
    _logger = logging.getLogger(__name__)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    # se retorna data -> objeto, error -> booleano
    def fetch_all(self, page=1, size=20):
        try:
            areas = db.session.query(Area).paginate(int(page), size)
            return (areas, False)
        except Exception as e:
            self._logger.error(f"Error al obtener todas los areas: {e}", exc_info=True)
            return ([], True)
    
    def fetch_by_id(self, id):
        try:
            area = db.session.query(Area).filter(Area.id_area == id).first()
            return (area, False)
        except Exception as e:
            self._logger.error(f"Error al obtener la area con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def create(self, data):

        try:
            new_area = Area(
                nombre = data['nombre'],
                clave_contable = data['clave_contable'],
                fecha_registro = datetime.now(),
                usuario_registro = data['usuario_registro'],
                activo = True
            )
            db.session.add(new_area)
            db.session.commit()
            return (new_area, False)
        except Exception as e:
            self._logger.error(f"Error al crear la area: {e}", exc_info=True)
            return (None, True)
        
    def update(self, id, data):
        try:
            area = db.session.query(Area).filter(Area.id_area == id).first()
            if not area:
                return (None, False)
            for key, value in data.items():
                setattr(area, key, value)
            area.fecha_modifico = datetime.now()
            db.session.commit()
            return (area, False)
        except Exception as e:
            self._logger.error(f"Error al actualizar la area con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def delete(self, id):
        try:
            area = db.session.query(Area).filter(Area.id_area == id).first()
            if not area:
                return False
            db.session.delete(area)
            db.session.commit()
            return True
            
        except Exception as e:
            self._logger.error(f"Error al eliminar la area con ID {id}: {e}", exc_info=True)
            return False
