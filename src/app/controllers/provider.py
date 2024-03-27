from flask_restx import (
    Resource,
    reqparse,
    Namespace,
    fields
)
from flask import request
from ..services.provider import ProviderService
from ..schemas.provider import ProviderSchema
from ..validators.provider import provider_post_model, provider_put_model
api = Namespace('Providers', description='Endpoints para mostrar información sobre Proveedores')

post_model = api.model('Provider', provider_post_model)
put_model = api.model('Provider', provider_put_model)


class ProviderListController(Resource):
    provider_service = ProviderService()
    providers_schema = ProviderSchema(many=True)
    provider_schema = ProviderSchema()

    parser_device = reqparse.RequestParser()
    parser_device.add_argument('page', type=int, help='La página solicitada')
    parser_device.add_argument('size', type=int, help='Cantidad de elementos por página')

    @api.doc(parser=parser_device, responses={200: 'Success', 404: 'Not Found'})
    def get(self):
        page = 1 if not request.args.get('page') else int(request.args.get('page'))
        size = 20 if not request.args.get('size') else int(request.args.get('size'))
        
        providers = []
        error_occurred = False
        providers, error_occurred = self.provider_service.fetch_all(page, size)

        if error_occurred:
            return {'data': [], 'status': 'Ha ocurrido un error, por favor intente más tarde'}, 500
        there_are_devices =  len(providers.items) > 0
        status_code_msg_status = {
            True: (200, "OK", providers.prev_num, providers.next_num, providers.total),
            False: (404, "No hay proveedores disponibles", 0, 0, 0)
        } 
        status_code, msg_status, prev, next, total = status_code_msg_status[there_are_devices]
        response = {
            'data': self.providers_schema.dump(providers.items),
            'prev': prev,
            'next': next,
            'count': total,   
            'statuts': msg_status,
        }, status_code
        return response

    @api.expect(post_model, validate=True)
    def post(self):
        data = request.get_json(force=True)
        new_provider, error = self.provider_service.create(data)
        #objeto, mensaje, status_code
        values_depends_on_error = {
            True: (None, 'Ha ocurrido un error, por favor intente más tarde', 500),
            False: (self.provider_schema.dump(new_provider), 'Creado con exito', 201)
        }
        data, status_msg, status_code = values_depends_on_error[error]
        response = {
            'data': data,
            'status': status_msg
        }, status_code
        return response
         

class ProviderController(Resource):
    provider_service = ProviderService()
    provider_schema = ProviderSchema()

    def get(self, id):
        provider, error = self.provider_service.fetch_by_id(id)
        if error:
            return {
                'data': None , 
                'status': 'Lo sentimos, ocurrio un error intente más tarde'
            }, 500
        status_code_msg_status = {
            True: (200, self.provider_schema.dump(provider), 'OK'),
            False: (404, None, 'No se encontro un proveedor con el id proporcionado')
        }
        status_code, employee_resp, msg_status = status_code_msg_status[employee is not None]
        return {'data': employee_resp, 'status': msg_status}, status_code
        
    @api.expect(put_model, validate=True)
    @api.doc(params={'id': 'ID del proveedor'})
    def put(self, id):
        if not self.provider_service.fetch_by_id(id)[0]:
            return {
                'data': None, 
                'status': 'Lo sentimos no se encontró el proveedor'
            }, 404
        data = request.get_json(force=True)
        provider, error = self.provider_service.update(id, data)
        device_msg_status_status_code = {
            True: (None, 'Error al actualizar el proveedor', 500),
            False: (self.provider_schema.dump(provider), 'Actualizado con exito', 200)
        }
        
        employee_resp, msg_status, status_code = device_msg_status_status_code[error]
        response = {
            'data': employee_resp,
            'status': msg_status
        }, status_code
        return response       

    def delete(self, id):
        provider_founded = self.provider_service.fetch_by_id(id)
        if not provider_founded[0]:
            return {
                'data': None, 
                'status': 'Lo sentimos no se encontró el proveedor'
            }, 404
        
        success = self.provider_service.delete(id)
        provider_msg_status_status_code = {
            True: (self.provider_schema.dump(provider_founded), 'Eliminado con exito', 200),
            False: (None, 'Error al eliminar el proveedor', 500)
        }
        provider, msg_status, status_code = provider_msg_status_status_code[success]
        response =  {
            'data': provider, 
            'status': msg_status
        }, status_code
        return response
