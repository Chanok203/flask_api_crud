from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.account import bp as account_bp

    app.register_blueprint(account_bp, url_prefix="/accounts")

    return app


from app import models  # isort:skip

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = models.User.get_by_username(username)
    if not user or not user.verify_password_hash(password) or not user.is_staff:
        return False
    g.user = user
    return True
