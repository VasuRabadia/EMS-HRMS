from flask import request, redirect, url_for, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from functools import wraps
import jwt
from datetime import datetime
from config import Config
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.cookies:
            try:
                token = str(request.cookies["Authorization"]).split(' ')[1]
            except Exception:
                token = str(request.cookies["Authorization"])
            is_valid = validate_jwt(token, Config.JWT_SECRET_KEY)
            if is_valid:
                return f(*args, **kwargs)
            else:
                return jsonify(redirect=url_for('home.home'), message="Session Timeout")
        else:
            return jsonify(redirect=url_for('home.home'), message="Unauthorized User")

    return decorated


def validate_jwt(token, secret_key):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

        expiration_time = decoded_token.get('exp')
        current_time = datetime.utcnow()
        valid_time = current_time < datetime.fromtimestamp(expiration_time)

        user = decoded_token.get('sub')
        valid_user = User.get_user(user)

        if not valid_time and not valid_user:
            return False

        return True

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError as e:
        return False


# permission_required()
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("permission_required f:",f)
            token = None
            print("token:",token)
            if "Authorization" in request.cookies:
                try:
                    token = str(request.cookies["Authorization"]).split(' ')[1]
                except Exception:
                    token = str(request.cookies["Authorization"])
                print("token:",token)
                valid_token = validate_jwt(token, Config.JWT_SECRET_KEY)
                print("valid_token:",valid_token)
                if valid_token:
                    decoded_token = jwt.decode(
                        token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                    print("decoded_token:",decoded_token)
                    user_identity = decoded_token.get('sub')
                    print("user_identity:",user_identity)
                    if check_user_permission(user_identity, permission):
                        print("IF TRUE")
                        return f(*args, **kwargs)
                    else:
                        print("IF FALSE")
                        return jsonify(redirect=url_for('home.home_header'), message="Permission Denied")
                else:
                    return jsonify(redirect=url_for('home.home'), message="Session Timeout")
            else:
                return jsonify(redirect=url_for('home.home'), message="Unauthorized User")
        return decorated_function
    return decorator


def check_user_permission(user_identity, permission):
    user = User.get_user_by_id(user_identity)
    print("user:",user)
    print("permission:",permission)
    if user['role'] == "Admin":
        return True
    elif user['role'] == "User":
        if permission == "show":
            return True
    return False


def decoded_token(token):
    try:
        decoded_token = jwt.decode(
            token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except Exception:
        return None
