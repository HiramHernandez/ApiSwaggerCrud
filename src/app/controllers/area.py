from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from ..services.area import AreaService
from ..schemas.area import AreaSchema
from ..validators.area import area_post_model, area_put_model
api = Namespace('Areas', description='Endpoints para mostrar información sobre las Areas')

post_model = api.model('Area', area_post_model)
put_model = api.model('Area', area_put_model)

class AreaListController(Resource):
    area_service = AreaService()
    areas_schema = AreaSchema(many=True)
    area_schema = AreaSchema()

    parser_device = reqparse.RequestParser()
    parser_device.add_argument('page', type=int, help='La página solicitada')
    parser_device.add_argument('size', type=int, help='Cantidad de elementos por página')

    @api.doc(parser=parser_device, responses={200: 'Success', 404: 'Not Found'})
    def get(self):
        page = 1 if not request.args.get('page') else int(request.args.get('page'))
        size = 20 if not request.args.get('size') else int(request.args.get('size'))
        
        error_occurred = False
        areas, error_occurred = self.area_service.fetch_all(page, size)

        if error_occurred:
            return {'data': [], 'status': 'Ha ocurrido un error, por favor intente más tarde'}, 500
        there_are_devices =  len(areas.items) > 0
        status_code_msg_status = {
            True: (200, "OK", areas.prev_num, areas.next_num, areas.total),
            False: (404, "No hay areas disponibles", 0, 0, 0)
        } 
        status_code, msg_status, prev, next, total = status_code_msg_status[there_are_devices]
        response = {
            'data': self.areas_schema.dump(areas.items),
            'prev': prev,
            'next': next,
            'count': total,   
            'statuts': msg_status,
        }, status_code
        return response

    @api.expect(post_model, validate=True)
    def post(self):
        data = request.get_json(force=True)
        new_area, error = self.area_service.create(data)
        #objeto, mensaje, status_code
        values_depends_on_error = {
            True: (None, 'Ha ocurrido un error, por favor intente más tarde', 500),
            False: (self.area_schema.dump(new_area), 'Creado con exito', 201)
        }
        data, status_msg, status_code = values_depends_on_error[error]
        response = {
            'data': data,
            'status': status_msg
        }, status_code
        return response
         

class AreaController(Resource):
    area_service = AreaService()
    area_schema = AreaSchema()

    def get(self, id):
        area, error = self.area_service.fetch_by_id(id)
        if error:
            return {
                'data': None , 
                'status': 'Lo sentimos, ocurrio un error intente más tarde'
            }, 500
        status_code_msg_status = {
            True: (200, self.area_schema.dump(area), 'OK'),
            False: (404, None, 'No se encontro un Area con el id proporcionado')
        }
        status_code, area_resp, msg_status = status_code_msg_status[area is not None]
        return {'data': area_resp, 'status': msg_status}, status_code
        
    @api.expect(put_model, validate=True)
    @api.doc(params={'id': 'ID de la Area'})
    def put(self, id):
        if not self.area_service.fetch_by_id(id)[0]:
            return {
                'data': None, 
                'status': 'Lo sentimos no se encontró la Area'
            }, 404
        data = request.get_json(force=True)
        area, success = self.area_service.update(id, data)
        area_msg_status_status_code = {
            True:  (None, 'Error al actualizar la Area', 500),
            False: (self.area_schema.dump(area), 'Actualizado con exito', 200)
        }
        
        area_resp, msg_status, status_code = area_msg_status_status_code[success]
        response = {
            'data': area_resp,
            'status': msg_status
        }, status_code
        return response       

    def delete(self, id):
        area_founded = self.area_service.fetch_by_id(id)
        if not area_founded[0]:
            return {
                'data': None, 
                'status': 'Lo sentimos no se encontró la Area'
            }, 404
        
        success = self.bank_service.delete(id)
        area_msg_status_status_code = {
            True: (self.area_schema.dump(area_founded), 'Eliminado con éxito', 200),
            False: (None, 'Error al eliminar el banco', 500)
        }
        area, msg_status, status_code = area_msg_status_status_code[success]
        response =  {
            'data': area, 
            'status': msg_status }, status_code
        return response
