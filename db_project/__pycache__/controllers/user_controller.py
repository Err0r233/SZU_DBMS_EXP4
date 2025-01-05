# dashboard
from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from utils.db import add_product

bp = Blueprint('user', __name__)

@bp.route('/dashboard')
@jwt_required(locations=["cookies"])
def dashboard():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    return render_template("dashboard.html", role=role, current_user=current_user)

# 上架产品页
@bp.route('/my_management', methods = ['GET', 'POST'])
@jwt_required(locations=["cookies"])
def my_management():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admins cannot upload products"}), 400
    return render_template("my_management.html", role=role, current_user = current_user)

# 上架产品
@bp.route('/upload_product', methods = ['POST'])
@jwt_required(locations=["cookies"])
def upload_product():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admins cannnot upload products"}), 400
    data = request.get_json()
    productName = data.get('productName')
    productCategory = data.get('productCategory')
    productDescription = data.get('productDescription')
    productOrigin = data.get('productOrigin')
    productPrice = data.get('productPrice')
    saleStartDate = data.get('saleStartDate')
    saleEndDate = data.get('saleEndDate')

    res = add_product(current_user, productCategory, productName, productDescription, productOrigin, productPrice, saleStartDate, saleEndDate)
    if "error" in res:
        return jsonify({"message": "product has existed"}), 400
    return jsonify({"message": "product uploaded successfully"}), 200