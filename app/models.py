from app import db
from flask_restful import url_for
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_staff = db.Column(db.Boolean(), default=(lambda: False), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_staff": self.is_staff,
            "url": url_for("account.user", id=self.id, _external=True),
        }

    @staticmethod
    def get_password_hash(password):
        return sha256.hash(password)

    def verify_password_hash(self, password):
        return sha256.verify(password, self.password_hash)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def get_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        return user

    @classmethod
    def get_all(cls):
        user_list = cls.query.all()
        return user_list
