import logging
from datetime import datetime
from sqlalchemy.sql import func
from ..config.extensions import db
from ..models.bank import Bank


class BankService:
    _instance = None
    _logger = logging.getLogger(__name__)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    # se retorna data -> objeto, error -> booleano
    def fetch_all(self, page=1, size=20):
        try:
            banks = db.session.query(Bank).paginate(int(page), size)
            return (banks, False)
        except Exception as e:
            self._logger.error(f"Error al obtener todos los bancos: {e}", exc_info=True)
            return ([], True)
    
    def fetch_by_id(self, id):
        try:
            bank = db.session.query(Bank).filter(Bank.id_banco == id).first()
            return (bank, False)
        except Exception as e:
            self._logger.error(f"Error al obtener el banco con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def create(self, data):
        try:
            nuevo_banco = Bank(
                nombre = data['nombre'],
                pagina_web = data['pagina_web'],
                fecha_registro = datetime.now(),
                usuario_registro = data['usuario_registro'],
                activo = True
            )
            db.session.add(nuevo_banco)
            db.session.commit()
            return (nuevo_banco, False)
        except Exception as e:
            self._logger.error(f"Error al crear el banco: {e}", exc_info=True)
            return (None, True)
        
    def update(self, id, data):
        try:
            bank = db.session.query(Bank).filter(Bank.id_banco == id).first()
            if not bank:
                return (None, False)
            for key, value in data.items():
                setattr(bank, key, value)
            bank.fecha_modifico = datetime.now()
            db.session.commit()
            return (bank, False)
        except Exception as e:
            self._logger.error(f"Error al actualizar el banco con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def delete(self, id):
        try:
            bank = db.session.query(Bank).filter(Bank.id_banco == id).first()
            if not bank:
                return False
            db.session.delete(bank)
            db.session.commit()
            return True
            
        except Exception as e:
            self._logger.error(f"Error al eliminar el banco con ID {id}: {e}", exc_info=True)
            return False
