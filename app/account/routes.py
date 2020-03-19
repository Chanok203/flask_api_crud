from app.account import bp, api
from .resources import UserListAPI, UserAPI

api.add_resource(UserListAPI, "/users")
api.add_resource(UserAPI, "/users/<int:id>", endpoint="user")
