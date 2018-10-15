from flask_restful import Resource
from flask import request
from werkzeug.security import check_password_hash
from utils import valid_email, valid_username, valid_password
from .models import User
from flask_jwt_extended import create_access_token


class Signup(Resource):
    def post(self):
        ''' Adda new user '''
        data = request.get_json()

        username = data['username']
        email = data["email"]
        password = data['password']

        if not valid_username(username):
            return {'message': 'Invalid username'}, 400

        if not valid_email(email):
            return {'message': 'Invalid email'}, 400

        if not valid_password(password):
            return {'message': 'Invalid password'}, 400

        if not valid_username(username):
            return {'message': 'Invalid username'}, 400

        if User().get_user_by_username(username):
            return {'message': 'username already in use'}, 400

        if User().get_user_by_email(email):
            return {'message': 'email already in use'}, 400

        user = User(username, email, password)

        user.add()

        return {'message': 'Account created successfully'}, 201


class Login(Resource):
    def post(self):
        ''' Existing user can login '''
        data = request.get_json()

        username = data['username']
        password = data['password']

        user = User().get_user_by_username(username)
        print(user)

        if not user:
            return {'message': 'user not found'}, 404

        if not check_password_hash(user.password, password):
            return {'message': 'Wrong password'}, 400

        token = create_access_token(user.username)
        return {
            'token': token,
            'message': f'You were successfully logged in {username}'
        }, 200
