from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from utils.db import make_order, show_carts, clear_carts, add_carts

# 实现下单、购物车等

bp = Blueprint('purchase', __name__)

@bp.route('/order', methods = ['POST'])
@jwt_required(locations=["cookies"])
def order():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admin cannot make order!"}), 400
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    make_order(product_name, quantity, current_user)
    return jsonify({"message":"make order successfully"}), 200


# 展示购物车
@bp.route('/my_cart')
@jwt_required(locations=["cookies"])
def cart():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "no carts for admin"}), 400
    products = show_carts(current_user)
    return render_template('my_cart.html', products=products, role=role)

# 添加到购物车
@bp.route('/add_to_cart', methods=['POST'])
@jwt_required(locations=["cookies"])
def add_to_carts():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "no carts for admin"}), 400
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    add_carts(product_name, quantity, current_user)
    return jsonify({"message" : "add_to_cart successfully"}), 200

@bp.route('/make_cart_order', methods = ['POST'])
@jwt_required(locations=["cookies"])
def cart_order():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admin cannot make order!"}), 400
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    make_order(product_name, quantity, current_user)
    clear_carts(product_name, current_user)
    return jsonify({"message":"make order successfully"}), 200

# 清除购物车
@bp.route('/remove_cart', methods = ['POST'])
@jwt_required(locations=["cookies"])
def remove_cart():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "admins do not need this function"}), 400
    product_name = request.form['product_name']
    clear_carts(product_name, current_user)
    return jsonify({"message": "clear cart successfully"}), 200