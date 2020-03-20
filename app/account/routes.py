from app.account import bp, api
from flask import request, g
from .resources import UserListAPI, UserAPI, UserLogin
from app import verify_password

api.add_resource(UserListAPI, "/users")
api.add_resource(UserAPI, "/users/<int:id>", endpoint="user")
api.add_resource(UserLogin, "/login")
