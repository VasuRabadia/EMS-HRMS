from flask import Blueprint, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
from .token_check import permission_required


delete_bp = Blueprint('delete', __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["Task-4"]
collection = db["Task-4-Collection"]


@delete_bp.route('/delete/<id>', methods=['GET'])
@permission_required('delete')
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify(redirect=url_for('home.home_header'), message="Deleted Successfully")
