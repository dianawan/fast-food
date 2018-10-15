from flask import request
from flask_jwt_extended import jwt_required
from .models import FoodItem
from flask_restful import Resource
from .models import FoodItem
from utils import valid_food_description, valid_food_name


class CreateFood(Resource):
    @jwt_required
    def post(self):
        '''create a food item'''

        data = request.get_json()
        name = data['name']
        description = data["description"]
        price = data['price']

        if FoodItem().get_food_by_name(name):
            return {'message': f'food with name {name} alredy exists'}

        if not valid_food_name(name):
            return {'message': "Food name is invalid"}, 400

        if not valid_food_description(description):
            return {'message': "invalid food description"}, 400

        if type(price) != int:
            return {'message': "Invalid price"}, 400

        fooditem = FoodItem(name, description, price)

        fooditem.add()

        return {"message": "Food item created"}, 201


class FoodItems(Resource):
    @jwt_required
    def get(self):
        '''return a list of created fooditems'''

        food_items = FoodItem().get_all_fooditems()
        return {
            "food_items": [food_item.serialize() for food_item in food_items]
        }, 200

