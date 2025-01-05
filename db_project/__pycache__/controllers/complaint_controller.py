from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from utils.db import show_history_orders, get_complaints, submit_complaints

bp = Blueprint('complaint', __name__)


# 展示历史订单并且可以点击投诉
@bp.route('/complaint')
@jwt_required(locations=["cookies"])
def show_history_order():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "no"}), 400
    products = show_history_orders(current_user)
    return render_template("complaint.html", role=role, products = products)

# 提交投诉
@bp.route('/submit_complaint', methods = ["POST"])
@jwt_required(locations=["cookies"])
def submit_complaint():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "no"}), 400
    product_name = request.form['product_name']
    make_order_time = request.form['make_order_time']
    complaint_reason = request.form['complaint_reason']
    submit_complaints(current_user, product_name, make_order_time, complaint_reason)
    return jsonify({"success": "submit order successfully"}), 200

# 查看投诉及处理
@bp.route('/see_complaint')
@jwt_required(locations=["cookies"])
def see_complaint():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    is_banned = get_jwt()['is_banned']
    if is_banned == "true":
        return jsonify({"message": "Your account has been frozen"}), 400
    if role == "admin":
        return jsonify({"message": "no"}), 400
    complaints = get_complaints(current_user)
    return render_template("see_complaint.html", role=role, complaints = complaints)