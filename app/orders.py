from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Order, FoodItem
from utils import valid_food_description, valid_food_name, valid_destination, valid_person_name


class PostOrder(Resource):
    @jwt_required
    def post(self, id):
        '''post an order by the user'''

        data = request.get_json()

        destination = data['destination']
        current_user = get_jwt_identity()

        food_item = FoodItem().get_food_by_id(id)

        if not food_item:
            return {"message": "food item not found"}, 404

        if not valid_destination(destination):
            return {"message": "please enter a valid destination"}, 400

        order = Order(current_user, destination, food_item.name,
                      food_item.price)

        order.add()

        return {"meassage": "order placed sucessfully"}, 201


class SpecificOrder(Resource):
    @jwt_required
    def get(self, id):
        '''get a specific order by id'''

        order = Order().get_by_id(id)

        if order:
            return {"order": order.serialize()}, 200

        return {"message": "Order not found"}, 404

    @jwt_required
    def delete(self, id):
        '''delete a specific order by id'''

        order = Order().get_by_id(id)

        if order:
            order.delete(id)
            return {"message": "order deleted successfully"}, 200
        return {"message": "Order not found"}, 404


class AcceptStatus(Resource):
    @jwt_required
    def put(self, id):
        '''mark an order as approved'''

        order = Order().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {
                    "message": "order already {}".format(order.status)
                }, 200
            order.accept_status(id)
            return {"message": "your order has been approved"}, 200
        return {"message": "order not found"}, 404


class GetOrders(Resource):
    @jwt_required
    def get(self):
        '''returnlist of placed orders'''
        orders = Order().get_all_foodorders()
        if orders:
            return {
                "placed_orders": [order.serialize() for order in orders]
            }, 200
        return {'message': 'orders not found'}, 404


class DeclineOrder(Resource):
    @jwt_required
    def put(self, id):
        '''decline a specific order'''

        order = Order().get_by_id(id)

        if order:

            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}

            order.decline_order(id)
            return {"message": "Order declined"}

        return {"message": "Order not found"}, 404


class CompleteOrder(Resource):
    def put(self, id):
        '''mark an order as completed by admin'''
        order = Order().get_by_id(id)

        if order:
            if order.status == "accepted":
                return {"message":"order already approved"},400
            if order.status == "completed" or order.status == "declined":
                return {"message": "order already {}".format(order.status)}

            if order.status == "Pending":
                return {"message": "please approve the order first "}

            if order.status == "approved":
                order.complete_accepted_order(id)
                return {
                    "message":
                    "Your has been order completed awaiting delivery"
                }

        return {"message": "Order not found"}, 404


class GetAcceptedOrders(Resource):
    '''Get the Orders accepted by admin'''

    def get(self):
        '''return list of approved orders'''

        approved_orders = Order().accepted_orders()
        if approved_orders:
            return {
                "approved_orders": [
                    approved_order.serialize()
                    for approved_order in approved_orders
                ]
            }, 200
        return {'message': 'There no approved orders'}, 404


class DeclinedOrders(Resource):
    def get(self):
        '''return all orders declined'''

        declined_orders = Order().accepted_orders()
        if declined_orders:
            return {
                "declined orders": [
                    declined_order.serialize()
                    for declined_order in declined_orders
                ]
            }, 200
        return {'message': 'There are no declined orders'}


class CompletedOrder(Resource):
    def get(self):
        '''return completed orders awaiting delivery'''
        declined_orders = Order().accepted_orders()
        if declined_orders:
            return {
                "declined orders": [
                    declined_order.serialize()
                    for declined_order in declined_orders
                ]
            }, 200
        return {'message': 'There are no completed orders'}
