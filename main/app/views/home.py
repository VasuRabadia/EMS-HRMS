from flask import Blueprint, render_template
from app import mongo
from .token_check import permission_required


home_bp = Blueprint('home', __name__, url_prefix='/')


@home_bp.route('/', methods=['GET'])
def home():
    return render_template("login.html")


@home_bp.route('/header', methods=['GET'])
@permission_required('show')
def home_header():
    # Select2
    query = {}
    projection = {'_id': 0, 'plan': 1}
    collection = mongo.db['Task-4-Collection']
    plan = list(collection.find(query, projection))
    plan_set = set()
    for p in plan:
        plan_set.add(p['plan'])
    return render_template("index.html", plans=list(plan_set))
