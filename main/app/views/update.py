from flask import Blueprint, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
from .token_check import permission_required


update_bp = Blueprint('update', __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["Task-4"]
collection = db["Task-4-Collection"]


@update_bp.route('/update/<id>', methods=['POST'])
@permission_required('update')
def update(id):
    collection.update_one({'_id': ObjectId(id)},
                          {"$set": {
                              'name': request.form.get('name', ''),
                              'reference_name': request.form.get('reference_name', ''),
                              'total_investment': request.form.get('total_investment', ''),
                              'plan': request.form.get('plan', ''),
                              'last_generated_date': request.form.get('last_generated_date', ''),
                              'mobile_number': request.form.get('mobile_number', ''),
                              'investment_date': request.form.get('investment_date', ''),
                              'city': request.form.get('city', ''),
                              'email': request.form.get('email', ''),
                              'age': request.form.get('age', ''),
                          }
    })
    return jsonify(redirect=url_for('home.home_header'), message="Updated Successfully")
    # return redirect('/header')
