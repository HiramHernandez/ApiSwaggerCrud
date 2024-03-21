from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from ..services.device import DeviceService, RecordService, MaintenanceService
from ..schemas.device import (
    DeviceSchema, 
    RecordSchema, 
    EnergySchema, 
    MaintenanceSchema
)
from ..validators.device import device_post_model
api = Namespace('Dispositivos y Registros', description='Endpoints para mostrar información sobre dispositivos y registros')

post_model = api.model('Device', device_post_model)

class DeviceListController(Resource):
    device_service = DeviceService()
    parser_device = reqparse.RequestParser()
    parser_device.add_argument('device_type_id', type=int, help='Buscar por ID Tipo Dispositivo')

    devices_schema = DeviceSchema(many=True)
    device_schema = DeviceSchema()


    @api.doc(parser=parser_device, responses={200: 'Success', 404: 'Not Found'})
    def get(self):
        devices = []
        error_occurred = False
        search_by_device_type = request.args.get("device_type_id") is not None
        if search_by_device_type:
            devices, error_occurred = self.device_service.fetch_by_type(request.args.get("device_type_id"))
        else:
            devices, error_occurred = self.device_service.fetch()
        
        if error_occurred:
            return {'data': [], 'statuts': 'Ha ocurrido un error, por favor intente más tarde'}, 500
        there_are_devices =  len(devices) > 0

        status_code_msg_status = {
            True: (200, "OK"),
            False: (404, "No hay dispositivos disponibles")
        } 
        status_code, msg_status = status_code_msg_status[there_are_devices]
        response = {
            'dispositivos': self.devices_schema.dump(devices),
            'statuts': msg_status,
        }, status_code
        return response

    @api.expect(post_model, validate=True)
    def post(self):
        data = request.get_json(force=True)
        new_device, error = self.device_service.create(data)
        #objeto, mensaje, status_code
        values_depends_on_error = {
            True: (None, 'Ha ocurrido un error, por favor intente más tarde', 500),
            False: (self.device_schema.dump(new_device), 'Creado con exito', 201)
        }
        data, status_msg, status_code = values_depends_on_error[error]
        response = {
            'dispositivo': data,
            'status': status_msg
        }, status_code
        return response
   

class DeviceController(Resource):
    device_service = DeviceService()
    device_schema = DeviceSchema()

    def get(self, id):
        device, error = self.device_service.retrieve(id)
        if error:
            return {
                'dispositivos': None , 
                'status': 'Lo sentimos, ocurrio un error intente más tarde'
            }, 500
        status_code_msg_status = {
            True: (200, self.device_schema.dump(device), 'OK'),
            False: (404, None, 'No se encontro un dispositivo con el id proporcionado')
        }
        status_code, device_resp, msg_status = status_code_msg_status[device is not None]
        return {'dispositivo': device_resp, 'status': msg_status}, status_code
        
    @api.expect(post_model, validate=True)
    @api.doc(params={'id': 'ID del dispositivo'})
    def put(self, id):
        if not self.device_service.retrieve(id)[0]:
            return {
                'dispositivo': None, 
                'status': 'Lo sentimos no se encontró dispositivo'
            }, 404
        data = request.get_json(force=True)
        device, success = self.device_service.update(id, data)
        device_msg_status_status_code = {
            True: (self.device_schema.dump(device), 'Actualizado con exito', 200),
            False: (None, 'Error al actualizar el dispositivo', 500)
        }
        
        device, msg_status, status_code = device_msg_status_status_code[success]
        response = {
            'dispositivo': device,
            'status': msg_status
        }, status_code
        return response
       

    def delete(self, id):
        device_founded = self.device_service.retrieve(id)
        if not device_founded[0]:
            return {
                'dispositivo': None, 
                'status': 'Lo sentimos no se encontró dispositivo'
            }, 404
        
        success = self.device_service.delete(id)
        device_msg_status_status_code = {
            True: (self.device_schema.dump(device_founded), 'Eliminado con exito', 200),
            False: (None, 'Error al eliminar el dispositivo', 500)
        }
        device, msg_status, status_code = device_msg_status_status_code[success]
        response =  {
            'dispositivo': device, 
            'status': msg_status }, status_code
        return response


class RecordListController(Resource):
    record_service = RecordService()
    device_service = DeviceService()
    parser_record = reqparse.RequestParser()
    parser_record.add_argument('device_type_id', type=int, help='Buscar por ID Tipo Dispositivo')
    parser_record.add_argument('device_id', type=int, help='Buscar por ID Dispositivo')
    record_schema = RecordSchema()
    records_schema = RecordSchema(many=True)


    @api.doc(parser=parser_record)
    def get(self):
        if request.args.get("device_type_id"):
            records = self.record_service.fetch_by_type(request.args.get("device_type_id"))
            return {'registros': self.records_schema.dump(records), 'status': 'Ok'}
        if request.args.get("device_id"):
            records = self.record_service.fetch_by_device(request.args.get("device_id"))
            return {'registros': self.records_schema.dump(records), 'status': 'Ok'}
        records = self.record_service.fetch()
        if not records:
            return {
                'registros': {} , 
                'status': 'Error al obtener todos los registros'
            }, 404
        return {'registros': records, 'status': 'Ok'}
       
    def post(self):
        data = request.json
        if self.device_service.device_is_in_maintence(data["dispositivo_id"]):
            return {
                'registro': {}, 
                'status': 'No se permite registros ya que el dispositivo esta en mantenimiento'
            }, 404
        new_record = self.record_service.create(data)
      
        if not new_record:
            return {
                'dispositivo': {} , 
                'status': 'Error al guardar el registro'
            }, 404
        return {'registro': self.record_schema.dump(new_record), 'status': 'Creado con exito'}, 201
        

class RecordController(Resource):
    record_service = RecordService()
    record_schema = RecordSchema()
    
    def get(self, id):
        record = self.record_service.retrieve(id)
        if not record:
            {
                'Registro': {} , 
                'status': 'No se encontro registro con el id proporcionado'
            }, 404
        return {'registro': self.record_schema.dump(record), 'status': 'Ok'}
        

    def put(self, id):
        data = request.json
        record = self.record_service.update(id, data)
        if not record:
            return {
                'registro': {} , 
                'status': 'Error al actualizar el registro'
            }, 404
        record_founded = self.record_service.retrieve(id)
        return {'registro': self.record_schema.dump(record_founded), 'status': 'Actualizado con exito'}
       

    def delete(self, id):
        record_founded = self.record_service.retrieve(id)
        if not record_founded:
            return {'registro': {}, 'status': 'El id ingresado no existe'}
        record = self.record_service.delete(id)
        if not record:
            return {
                'registro': {} , 
                'status': 'Error al eliminar el registro'
            }, 404
        return {'registro': self.record_schema.dump(record_founded), 'status': 'Eliminado con exito'} 
            
      
class TotalEnergyController(Resource):
    record_service = RecordService()
    energy_schema = EnergySchema()

    def get(self):
        energy = self.record_service.total_energy()
        if not energy:
            return {
                'Registro': {} , 
                'status': 'No se encontraron registros de energia'
            }, 404
        return {'energia': self.energy_schema.dump(energy), 'status': 'Ok'}


class MaintenanceListController(Resource):
    maintenance_service = MaintenanceService()
    maintances_schema = MaintenanceSchema(many=True)
    maintance_schema = MaintenanceSchema()

    def get(self):
        maintenance_devices = self.maintenance_service.fetch()
        if maintenance_devices:
            return {
                'registros': {} , 
                'status': 'Error al obtener todos los dispositivos en mantenimiento'
            }, 404
        return {'dispositivos': self.maintances_schema.dump(maintenance_devices), 'status': 'Ok'}
        

    def post(self):
        data = request.json
        new_maintenance_device = self.maintenance_service.create(data)
        if not new_maintenance_device:
            return {
                'dispositivo': {} , 
                'status': 'Error al guardar el dispositivo en mantenimiento'
            }, 404
        return {'dispositivo': self.maintance_schema.dump(new_maintenance_device), 'status': 'Creado con exito'}, 201
        


class MaintenanceController(Resource):
    maintenance_service = MaintenanceService()
    maintance_schema = MaintenanceSchema()

    def get(self, device_id):
        maintenance_device = self.maintenance_service.retrieve(device_id)
        if not maintenance_device:
            return {
                'registros': {} , 
                'status': 'No se encontraron dispositivos en mantenimiento con el id ingresado'
            }, 404
        return {'dispositivo': self.maintance_schema.dump(maintenance_device), 'status': 'Ok'}
