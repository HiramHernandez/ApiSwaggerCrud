from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from ..services.bank import BankService
from ..schemas.bank import BankSchema
from ..validators.bank import bank_post_model, bank_put_model
api = Namespace('Bancos', description='Endpoints para mostrar información sobre bancos')

post_model = api.model('Bank', bank_post_model)
put_model = api.model('Bank', bank_put_model)

class BankListController(Resource):
    bank_service = BankService()
    banks_schema = BankSchema(many=True)
    bank_schema = BankSchema()

    parser_device = reqparse.RequestParser()
    parser_device.add_argument('page', type=int, help='La página solicitada')
    parser_device.add_argument('size', type=int, help='Cantidad de elementos por página')

    @api.doc(parser=parser_device, responses={200: 'Success', 404: 'Not Found'})
    def get(self):
        page = 1 if not request.args.get('page') else int(request.args.get('page'))
        size = 20 if not request.args.get('size') else int(request.args.get('size'))
        
        error_occurred = False
        banks, error_occurred = self.bank_service.fetch_all(page, size)

        if error_occurred:
            return {'data': [], 'status': 'Ha ocurrido un error, por favor intente más tarde'}, 500
        there_are_devices =  len(banks.items) > 0
        status_code_msg_status = {
            True: (200, "OK", banks.prev_num, banks.next_num, banks.total),
            False: (404, "No hay bancos disponibles", 0, 0, 0)
        } 
        status_code, msg_status, prev, next, total = status_code_msg_status[there_are_devices]
        response = {
            'data': self.banks_schema.dump(banks.items),
            'prev': prev,
            'next': next,
            'count': total,   
            'statuts': msg_status,
        }, status_code
        return response

    @api.expect(post_model, validate=True)
    def post(self):
        data = request.get_json(force=True)
        new_bank, error = self.bank_service.create(data)
        #objeto, mensaje, status_code
        values_depends_on_error = {
            True: (None, 'Ha ocurrido un error, por favor intente más tarde', 500),
            False: (self.bank_schema.dump(new_bank), 'Creado con exito', 201)
        }
        data, status_msg, status_code = values_depends_on_error[error]
        response = {
            'data': data,
            'status': status_msg
        }, status_code
        return response
         

class BankController(Resource):
    bank_service = BankService()
    bank_schema = BankSchema()

    def get(self, id):
        bank, error = self.bank_service.fetch_by_id(id)
        if error:
            return {
                'data': None , 
                'status': 'Lo sentimos, ocurrio un error intente más tarde'
            }, 500
        status_code_msg_status = {
            True: (200, self.bank_schema.dump(bank), 'OK'),
            False: (404, None, 'No se encontro un banco con el id proporcionado')
        }
        status_code, bank_resp, msg_status = status_code_msg_status[bank is not None]
        return {'data': bank_resp, 'status': msg_status}, status_code
        
    @api.expect(put_model, validate=True)
    @api.doc(params={'id': 'ID del banco'})
    def put(self, id):
        if not self.bank_service.fetch_by_id(id)[0]:
            return {
                'data': None, 
                'status': 'Lo sentimos no se encontró el banco'
            }, 404
        data = request.get_json(force=True)
        bank, success = self.bank_service.update(id, data)
        bank_msg_status_status_code = {
            True: (None, 'Error al actualizar el banco', 500),
            False: (self.bank_schema.dump(bank), 'Actualizado con exito', 200)
        }
        
        bank_resp, msg_status, status_code = bank_msg_status_status_code[success]
        response = {
            'data': bank_resp,
            'status': msg_status
        }, status_code
        return response       

    def delete(self, id):
        bank_founded = self.bank_service.fetch_by_id(id)
        if not bank_founded[0]:
            return {
                'data': None, 
                'status': 'Lo sentimos no se encontró el banco'
            }, 404
        
        success = self.bank_service.delete(id)
        bank_msg_status_status_code = {
            True: (self.bank_schema.dump(bank_founded), 'Eliminado con éxito', 200),
            False: (None, 'Error al eliminar el banco', 500)
        }
        bank, msg_status, status_code = bank_msg_status_status_code[success]
        response =  {
            'data': bank, 
            'status': msg_status }, status_code
        return response
