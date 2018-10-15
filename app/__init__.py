from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import app_config
from .orders import SpecificOrder, PostOrder, GetOrders, DeclineOrder, AcceptStatus, GetAcceptedOrders, DeclinedOrders, CompleteOrder, CompletedOrder
from .fooditems import FoodItems, CreateFood
from app.auth import Login, Signup

jwt = JWTManager()


def create_app(config_stage):
    app = Flask(__name__)
    app.config.from_object(app_config[config_stage])

    jwt.init_app(app)

    api = Api(app)

    api.add_resource(Signup, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(SpecificOrder, '/api/v1/orders/<int:id>')
    api.add_resource(CreateFood, '/api/v1/fooditem')
    api.add_resource(PostOrder, '/api/v1/fooditems/<int:id>/orders')
    api.add_resource(FoodItems, '/api/v1/fooditems')
    api.add_resource(GetOrders, '/api/v1/orders')
    api.add_resource(DeclineOrder, '/api/v1/orders/<int:id>/decline')
    api.add_resource(AcceptStatus, '/api/v1/orders/<int:id>/approve')
    api.add_resource(GetAcceptedOrders, '/api/v1/orders/approved')
    api.add_resource(DeclinedOrders, '/api/v1/orders/declined')
    api.add_resource(CompleteOrder, '/api/v1/orders/<int:id>/complete')
    api.add_resource(CompletedOrder, '/api/v1/orders/completed')
    # api.add_resource(FoodItems, '/api/v1/fooditems/<int:id>/delete')

    return app
