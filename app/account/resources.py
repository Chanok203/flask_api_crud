from flask_restful import Resource, reqparse, inputs
from app.models import User
from app import auth


class UserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("password", type=str)
        self.parser.add_argument("is_staff", type=inputs.boolean, default=False)

    @auth.login_required
    def get(self, id):
        user = User.get_by_id(id)
        if user:
            return {"user": user.to_json()}, 200
        return {"message": "ไม่พบผู้ใช้นี้"}, 404

    @auth.login_required
    def put(self, id):
        user = User.get_by_id(id)
        if user:
            data = self.parser.parse_args()
            password = data["password"]
            is_staff = data["is_staff"]

            if password:
                user.password_hash = User.get_password_hash(password)

            if is_staff:
                user.is_staff = is_staff

            try:
                user.save()
                return {"user": user.to_json()}, 200
            except:
                return {"message": "ไม่สามารถแก้ไขผู้ใช้ได้"}, 500

        return {"message": "ไม่พบผู้ใช้นี้"}, 404

    @auth.login_required
    def delete(self, id):
        user = User.get_by_id(id)
        if user:
            try:
                user.delete()
                return {"message": "ลบผู้ใช้เรียบร้อยแล้ว"}, 200
            except:
                return {"message": "ไม่สามารถลบผู้ใช้ได้"}, 500

        return {"message": "ไม่พบผู้ใช้นี้"}, 404


class UserListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("username", type=str, required=True)
        self.parser.add_argument("password", type=str, required=True)
        self.parser.add_argument("is_staff", type=inputs.boolean, default=False)

    @auth.login_required
    def get(self):
        user_list = [user.to_json() for user in User.get_all()]
        return {"users": user_list}

    @auth.login_required
    def post(self):
        data = self.parser.parse_args()
        username = data["username"]
        password = data["password"]
        is_staff = data["is_staff"]

        if User.get_by_username(username):
            return {"message": "ชื่อผู้ใช้นี้มีอยู่แล้ว"}, 409

        user = User(
            username=username,
            password_hash=User.get_password_hash(password),
            is_staff=is_staff,
        )

        try:
            user.save()
            return user.to_json(), 201
        except:
            return {"message": "ไม่สามารถสร้างชื่อผู้ใช้ได้"}, 500
