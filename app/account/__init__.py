from flask import Blueprint
from flask_restful import Api


bp = Blueprint("account", __name__)
api = Api(bp)

from app.account import routes
