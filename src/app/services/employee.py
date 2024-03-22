import logging
from datetime import datetime
from sqlalchemy.sql import func
from ..config.extensions import db
from ..models.employee import Employee


class EmployeService:
    _instance = None
    _logger = logging.getLogger(__name__)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    # se retorna data -> objeto, error -> booleano
    def fetch_all(self, page=1, size=20):
        try:
            empleados = db.session.query(Employee).paginate(int(page), size)
            
            return (empleados, False)
        except Exception as e:
            self._logger.error(f"Error al obtener todos los empleados: {e}", exc_info=True)
            return ([], True)
    
    def fetch_by_id(self, id):
        try:
            empleado = db.session.query(Employee).filter(Employee.id_empleado == id).first()
            return (empleado, False)
        except Exception as e:
            self._logger.error(f"Error al obtener el empleado con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def create(self, data):
        try:
            nuevo_empleado = Employee(
                nombre=data['nombre'],
                apellido_paterno=data['apellido_paterno'],
                apellido_materno=data['apellido_materno'],
                calle=data['calle'],
                numero=data['numero'],
                colonia=data['colonia'],
                ciudad=data['ciudad'],
                estado=data['estado'],
                codigo_postal=data['codigo_postal'],
                correo=data['correo'],
                telefono=data['telefono'],
                rfc=data['rfc'],
                curp=data['curp'],
                imss=data['imss'],
                tipo_sangre=data['tipo_sangre'],
                usuario=data['usuario'],
                contrasenia=data['contrasenia'],
                fecha_registro=datetime.now(),
                activo=True
            )
            db.session.add(nuevo_empleado)
            db.session.commit()
            return (nuevo_empleado, False)
        except Exception as e:
            self._logger.error(f"Error al crear el empleado: {e}", exc_info=True)
            return (None, True)
        
    def update(self, id, data):
        try:
            empleado = db.session.query(Employee).filter(Employee.id_empleado == id).first()
            if not empleado:
                return (None, False)
            for key, value in data.items():
                setattr(empleado, key, value)
            empleado.fecha_modifico = datetime.now()
            db.session.commit()
            return (empleado, False)
        except Exception as e:
            self._logger.error(f"Error al actualizar el empleado con ID {id}: {e}", exc_info=True)
            return (None, True)
        
    def delete(self, id):
        try:
            empleado = db.session.query(Employee).filter(Employee.id_empleado == id).first()
            if not empleado:
                return False
            db.session.delete(empleado)
            db.session.commit()
            return True
            
        except Exception as e:
            self._logger.error(f"Error al eliminar el empleado con ID {id}: {e}", exc_info=True)
            return False