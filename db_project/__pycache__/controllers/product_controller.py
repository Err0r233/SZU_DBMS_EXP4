from flask import request, jsonify, render_template, Blueprint,redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from utils.db import show_all_products, show_my_products, add_favorites, show_my_favorite, remove_my_favorite

bp = Blueprint('product', __name__)

# 实现查看所有产品和查看自己的产品

@bp.route('/product_management')
@jwt_required(locations=["cookies"])
def dashboard():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    products = show_all_products()
    if products == None:
        return render_template("product_management.html", role=role, current_user=current_user)
    else:
        return render_template("product_management.html", role=role, current_user=current_user, products = products)

@bp.route('/my_inventory')
@jwt_required(locations=["cookies"])
def inventory():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    products = show_my_products(current_user)
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return redirect('/dashboard')
    else:
        return render_template("my_product.html", inventory=products, role = role)

# 实现收藏功能
@bp.route('/add_to_favorites', methods=["POST"])
@jwt_required(locations=["cookies"])
def add_favorite():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admins do not need this function"}), 400
    product_name = request.form['product_name']
    res = add_favorites(product_name, current_user)
    if "error" in res:
        return jsonify({"message": "this object has already in your favorite collection"}), 400
    else:
        return jsonify({"message": "added successfully"}), 200

# 展示收藏页
@bp.route('/my_favorite')
@jwt_required(locations=["cookies"])
def my_favorite():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    products = show_my_favorite(current_user)
    if role == "admin":
        return redirect('/dashboard')
    else:
        return render_template("my_favorite.html", products=products, role = role)

# 移除收藏
@bp.route('/remove_favorite', methods=["POST"])
@jwt_required(locations=["cookies"])
def remove_favorite():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admins do not need this function"}), 400
    product_name = request.form['product_name']
    remove_my_favorite(current_user, product_name)
    return jsonify({"message": "remove favorite successfully"}), 200