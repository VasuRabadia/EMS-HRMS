from flask_pymongo import pymongo
from bson import ObjectId
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def create_user(email, password, role):
        user_collection = mongo.db.users
        password_hash = generate_password_hash(password)
        user_id = user_collection.insert_one(
            {'email': email, 'password': password_hash, 'role': role}).inserted_id
        return user_id

    @staticmethod
    def get_user(email):
        user_collection = mongo.db.users
        try:
            user_data = user_collection.find_one({'email': email})
            return user_data
        except Exception as e:
            return False

    @staticmethod
    def get_user_by_id(id):
        user_collection = mongo.db.users
        try:
            user_data = user_collection.find_one({'_id': ObjectId(id)})
            return user_data
        except Exception as e:
            return False

    @staticmethod
    def valid(user_data):
        email = user_data['email']
        password = user_data['password']
        user = User.get_user(email)
        try:
            if check_password_hash(user['password'], password):
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def delete(id):
        user_collection = mongo.db.users
        try:
            user_collection.delete_one({'_id': ObjectId(id)})
            return True
        except Exception:
            return False

    @staticmethod
    def permission(id, per):
        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': id})
        if user['role'] == "admin":
            return True
        else:
            if per == "show":
                return True
            else:
                return False
