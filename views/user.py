from flask import request
from flask_restx import Resource, Namespace
from container import user_service
from dao.model.user import User
from dao.model.user import UserSchema
from decorators.user import admin_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        user_service.create(request.json)
        return "", 201, {"location": f"/users/{User.id}"}


@user_ns.route('/<int:uid>')
class UserViews(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        res = UserSchema().dump(user)
        return res, 200

    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
