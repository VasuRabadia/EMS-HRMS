from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pymongo
import re
from .token_check import permission_required


data_bp = Blueprint('data', __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["Task-4"]
collection = db["Task-4-Collection"]
users = db["users"]


@data_bp.route('/getdata', methods=['POST'])
@permission_required('show')
def getData():
    print("GET_DATA")
    query = {}
    name_search = request.form.get("columns[1][search][value]", "")
    reference_name_search = request.form.get("columns[2][search][value]", "")
    total_investment_search = request.form.get("columns[3][search][value]", "")
    plan_search = request.form.get("columns[4][search][value]", "")
    last_generated_date_search = request.form.get(
        "columns[5][search][value]", "")
    mobile_number_search = request.form.get("columns[6][search][value]", "")
    city_search = request.form.get("columns[7][search][value]", "")
    investment_date_search = request.form.get("columns[8][search][value]", "")
    email_search = request.form.get("columns[9][search][value]", "")
    age_search = request.form.get("columns[10][search][value]", "")
    if name_search != "":
        query["name"] = {"$regex": name_search, "$options": "i"}
    if reference_name_search != "":
        query["reference_name"] = {
            "$regex": reference_name_search, "$options": "i"}
    if total_investment_search != "":
        query["total_investment"] = {
            "$regex": total_investment_search, "$options": "i"}
    if plan_search != "":
        query["plan"] = {
            "$regex": plan_search, "$options": "i"}
    if last_generated_date_search != "":
        query["last_generated_date"] = {
            "$regex": last_generated_date_search, "$options": "i"}
    if mobile_number_search != "":
        query["mobile_number"] = {
            "$regex": mobile_number_search, "$options": "i"}
    if city_search != "":
        query["city"] = {"$regex": city_search, "$options": "i"}
    if investment_date_search != "":
        query["investment_date"] = {
            "$regex": investment_date_search, "$options": "i"}
    if email_search != "":
        query["email"] = {"$regex": email_search, "$options": "i"}
    if age_search != "":
        query["age"] = {"$regex": age_search, "$options": "i"}

    search_value = request.form.get("search[value]")
    # Column mapping for sorting
    column_map = {
        1: "name",
        2: "reference_name",
        3: "total_investment",
        4: "plan",
        5: "last_generated_date",
        6: "mobile_number",
        7: "city",
        8: "investment_date",
        9: "email",
        10: "age"
    }

    try:
        order_column_index = int(request.form.get("order[0][column]"))
        order_column_name = column_map.get(order_column_index, "name")
        order_dir = request.form.get("order[0][dir]", "asc")
        sort_order = pymongo.ASCENDING if order_dir == "asc" else pymongo.DESCENDING
    except Exception as ex:
        order_column_index = 1
        order_column_name = column_map.get(order_column_index, "name")
        sort_order = pymongo.ASCENDING

    try:
        page = int(request.form.get("start", 0))
        page_size = int(request.form.get("length", 10))
    except ValueError:
        page = 0
        page_size = 10
    skip = page
    if search_value:
        regex = re.compile(f".*{re.escape(search_value)}.*", re.IGNORECASE)
        query = {
            "$or": [
                {"name": {"$regex": regex}},
                {"city": {"$regex": regex}},
            ]
        }
    try:
        total_records = collection.count_documents(query)
        data_list = list(collection.find(query).sort(
            order_column_name, sort_order).skip(skip).limit(page_size))
    except Exception as ex:
        total_records = 0
        data_list = []

    for data in data_list:
        data["_id"] = str(data["_id"])

    response = {
        "data": data_list,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
    }
    return jsonify(response)


@data_bp.route('/getdata/<id>', methods=['GET'])
@permission_required('show')
def get_data_by_id(id):
    print("GET_DATA_ID")
    data = collection.find_one({'_id': ObjectId(id)})
    if data:
        data['_id'] = str(data['_id'])
        # print(data)
        return jsonify(data)
    else:
        return jsonify({'message': 'Document not found'}), 404
