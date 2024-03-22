from flask import Blueprint
from flask_restx import Api
from src.app.controllers.device import (
    DeviceListController,
    DeviceController,
    RecordListController,
    RecordController,
    TotalEnergyController,
    MaintenanceListController,
    MaintenanceController
)
from .controllers.device import api as ns1
from .controllers.employee import (
    api as ns2,
    EmployeeController,
    EmployeeListController,
    LoginController
)

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_blueprint,
    title = 'Energia API',
    version = '1.0',
    description='REST API para visualizar dispositivos y sus registros.',
)
# namespace and controllers about devices
api.add_namespace(ns1)

api.add_resource(DeviceListController, '/devices')
api.add_resource(DeviceController, '/device/<int:id>')

api.add_resource(RecordListController, '/records')
api.add_resource(RecordController, '/record/<int:id>')

api.add_resource(TotalEnergyController, '/energy')

api.add_resource(MaintenanceListController, '/maintenance/devices')
api.add_resource(MaintenanceController, '/maintenance/device/<int:device_id>')

# namespace and controllers about employees
api.add_namespace(ns2)
api.add_resource(EmployeeListController, '/employees')
api.add_resource(EmployeeController, '/employee/<int:id>')
api.add_resource(LoginController, '/login')

