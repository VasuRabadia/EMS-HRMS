from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.models import User
from .token_check import decoded_token
from config import Config


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if User.get_user(email):
        return jsonify({"msg": "User already exists"}), 409

    user_id = User.create_user(email, password, role)

    return redirect(url_for("home.home"))


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user_data = {"email": email, "password": password}

    is_valid = User.valid(user_data)
    if not is_valid:
        return jsonify({"msg": "Bad email or password"}), 401

    user_data = User.get_user(email)
    if user_data["role"] == "Admin":
        access_token = create_access_token(
            identity=str(user_data["_id"]),
            additional_claims={"is_user": False, "is_admin": True},
            expires_delta=timedelta(minutes=30),
        )
    else:
        access_token = create_access_token(
            identity=str(user_data["_id"]),
            additional_claims={"is_user": True, "is_admin": False},
            expires_delta=timedelta(minutes=30),
        )

    response = redirect(url_for("home.home_header"))
    response.set_cookie("Authorization", f"{access_token}", httponly=True)
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged Out", "redirect": url_for("home.home")})
    response.delete_cookie("Authorization")
    return response
