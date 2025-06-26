from flask import Blueprint, request, redirect, url_for, jsonify
from pymongo import MongoClient
from .token_check import permission_required

create_bp = Blueprint('create', __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["Task-4"]
collection = db["Task-4-Collection"]


@create_bp.route('/create', methods=['POST'])
@permission_required('create')
def create():
    print("CREATE")
    name = (request.form.get('name')).title()
    reference_name = (request.form.get('reference_name')).title()
    total_investment = int(request.form.get('total_investment'))
    plan = (request.form.get('plan')).title()
    last_generated_date = (request.form.get('last_generated_date'))
    mobile_number = (request.form.get('mobile_number'))
    investment_date = (request.form.get('investment_date'))
    city = (request.form.get('city')).title()
    email = (request.form.get('email'))
    age = int(request.form.get('age'))
    new_entry = {
        "name": name,
        "reference_name": reference_name,
        "total_investment": total_investment,
        "plan": plan,
        "last_generated_date": last_generated_date,
        "mobile_number": mobile_number,
        "investment_date": investment_date,
        "city": city,
        "email": email,
        "age": age
    }
    collection.insert_one(new_entry)
    return jsonify(redirect=url_for('home.home_header'), message="Created Successfully")
