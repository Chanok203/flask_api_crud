from flask import Blueprint
from flask_restful import Api


bp = Blueprint("account", __name__)
api = Api(bp, prefix="/api/v1")

from app.account import routes
