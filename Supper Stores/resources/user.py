from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            fullname=user_data.get("fullname"),
            address=user_data.get("address"),
            phone=user_data.get("phone"),
            timestamp=user_data.get("timestamp"),
            username=user_data.get("username")
        )
        
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "email": user.email,
                "user": user.username,
                "fullname": user.fullname,
                "id": user.id,
            }, 200

        abort(401, message="Invalid credentials.")


@blp.route("/user/<int:user_id>")
class UserInfo(MethodView):
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User has been deleted successfully"}), 201

    @blp.response(200, UserSchema(many=True))
    def get(self, user_id):
        user = UserModel.query.get(user_id)

        if user:
            return jsonify(UserSchema().dump(user))
        else:
            abort(404, message="User not found")
