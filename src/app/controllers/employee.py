from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from ..services.employee import EmployeService
from ..helpers.token_helper import create_token
from ..schemas.employee import EmployeeSchema
from ..validators.employee import employee_post_model, employee_login_model
api = Namespace('Empleados', description='Endpoints para mostrar información sobre dispositivos y registros')

post_model = api.model('Employee', employee_post_model)
login_model = api.model('Login', employee_login_model)

class EmployeeListController(Resource):
    employee_service = EmployeService()
    employees_schema = EmployeeSchema(many=True)
    employee_schema = EmployeeSchema()

    parser_device = reqparse.RequestParser()
    parser_device.add_argument('page', type=int, help='La página solicitada')
    parser_device.add_argument('size', type=int, help='Cantidad de elementos por página')

    @api.doc(parser=parser_device, responses={200: 'Success', 404: 'Not Found'})
    def get(self):
        page = 1 if not request.args.get('page') else int(request.args.get('page'))
        size = 20 if not request.args.get('size') else int(request.args.get('size'))
        
        employees = []
        error_occurred = False
        employees, error_occurred = self.employee_service.fetch_all(page, size)

        if error_occurred:
            return {'data': [], 'status': 'Ha ocurrido un error, por favor intente más tarde'}, 500
        there_are_devices =  len(employees.items) > 0
        status_code_msg_status = {
            True: (200, "OK", employees.prev_num, employees.next_num, employees.total),
            False: (404, "No hay empleados disponibles", 0, 0, 0)
        } 
        status_code, msg_status, prev, next, total = status_code_msg_status[there_are_devices]
        response = {
            'empleados': self.employees_schema.dump(employees.items),
            'prev': prev,
            'next': next,
            'count': total,   
            'statuts': msg_status,
        }, status_code
        return response

    @api.expect(post_model, validate=True)
    def post(self):
        data = request.get_json(force=True)
        new_employee, error = self.employee_service.create(data)
        #objeto, mensaje, status_code
        values_depends_on_error = {
            True: (None, 'Ha ocurrido un error, por favor intente más tarde', 500),
            False: (self.employee_schema.dump(new_employee), 'Creado con exito', 201)
        }
        data, status_msg, status_code = values_depends_on_error[error]
        response = {
            'empleado': data,
            'status': status_msg
        }, status_code
        return response
         

class EmployeeController(Resource):
    employee_service = EmployeService()
    employee_schema = EmployeeSchema()

    def get(self, id):
        employee, error = self.employee_service.fetch_by_id(id)
        if error:
            return {
                'empleado': None , 
                'status': 'Lo sentimos, ocurrio un error intente más tarde'
            }, 500
        status_code_msg_status = {
            True: (200, self.employee_schema.dump(employee), 'OK'),
            False: (404, None, 'No se encontro un empleado con el id proporcionado')
        }
        status_code, employee_resp, msg_status = status_code_msg_status[employee is not None]
        return {'dispositivo': employee_resp, 'status': msg_status}, status_code
        
    @api.expect(post_model, validate=True)
    @api.doc(params={'id': 'ID del empleado'})
    def put(self, id):
        if not self.employee_service.retrieve(id)[0]:
            return {
                'empleado': None, 
                'status': 'Lo sentimos no se encontró el empleado'
            }, 404
        data = request.get_json(force=True)
        employee, success = self.employee_service.update(id, data)
        device_msg_status_status_code = {
            True: (self.employee_schema.dump(employee), 'Actualizado con exito', 200),
            False: (None, 'Error al actualizar el empleado', 500)
        }
        
        employee_resp, msg_status, status_code = device_msg_status_status_code[success]
        response = {
            'empleado': employee_resp,
            'status': msg_status
        }, status_code
        return response       

    def delete(self, id):
        employee_founded = self.employee_service.retrieve(id)
        if not employee_founded[0]:
            return {
                'empleado': None, 
                'status': 'Lo sentimos no se encontró el empleado'
            }, 404
        
        success = self.device_service.delete(id)
        employee_msg_status_status_code = {
            True: (self.employee_schema.dump(employee_founded), 'Eliminado con exito', 200),
            False: (None, 'Error al eliminar el dispositivo', 500)
        }
        employee, msg_status, status_code = employee_msg_status_status_code[success]
        response =  {
            'dispositivo': employee, 
            'status': msg_status }, status_code
        return response


class LoginController(Resource):
    employee_service = EmployeService()

    @api.expect(login_model, validate=True)
    def post(self):
        data = request.get_json(force=True)
        employee, error = self.employee_service.login(data['usuario'], data['contrasenia'])
        if error:
            return {
                'status': 'Ocurrio un error intente más tarde'
            }, 500
        if employee is None:
            return {
                'token': 'No fue posible',
                'status': 'Intente de nuevo error en usuario o contraseña'
            }, 200

        return {
            'token': create_token(employee),
            'status': 'Ok'
        }, 200


class LoginTestController(Resource):

    @api.expect(login_model, validate=True)
    def post(self):
        data =  request.get_json(force=True)
        if data['usuario'] != 'admin' or  data['contrasenia'] != 'admin':
            return {
                'empleado': None, 
                'status': 'Lo sentimos no se encontró el empleado'
            }, 404
        permisions = [
            {'action': 'read'},
            {'action': 'create'},
            {'action': 'update'},
            {'action': 'delete'}
        ]
        from flask_jwt_extended import create_access_token
        token = create_access_token(identity=17)
        print(token)
        from jwt import decode
        txt = decode(token, 'super-secret')
        print(txt)
        return {
            'token': token,
            'status': 'Ok'
        }, 200
    
