from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from utils.db import show_all_users, set_ban, set_unban, show_all_complaint_admin, update_complaint, _withdraw

bp = Blueprint('admin', __name__)
# 管理员处理投诉、封禁账号、下架产品处

'''
用户管理路由 /user_management，用于封禁用户。
需要列出users里的所有用户、是否被封禁等状态
功能：封禁账户、解封账户
'''
@bp.route('/user_management')
@jwt_required(locations=["cookies"])
def admin():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    if role == 'user':
        return jsonify({"message": "No Permission"}), 401
    users = show_all_users()
    return render_template("user_management.html", users = users)


'''
/update_ban_status用于更新用户的封禁状态
接受post参数:
ban = true/false
ban_reason = text
username = 123
因此需要创建一个banned_user表，同时设置触发器，当插入一条新数据的时候自动更新users表的is_banned状态
再设置一个触发器，当删除一条数据的时候自动更新users表的对应user的is_banned状态
'''
@bp.route('/update_ban_status', methods = ["POST"])
@jwt_required(locations=["cookies"])
def upd_ban():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    if role == 'user':
        return jsonify({"message": "No Permission"}), 401
    is_banned = request.form['ban']
    if "ban_reason" not in request.form:
        ban_reason = "123"
    else:
        ban_reason = request.form['ban_reason']
    banned_username = request.form['username']
    if is_banned == "true":
        res = set_ban(banned_username, ban_reason)
        if "error" in res:
            return jsonify({"message": "failed"}), 400
        return jsonify({"message": "ok"}), 200
    else:
        res = set_unban(banned_username)
        if "error" in res:
            return jsonify({"message": "failed"}), 400
        return jsonify({"message": "ok"}), 200

'''
投诉管理/complaint_management
展示my_complaint中的所有投诉，按钮点击更新处理意见。

'''
@bp.route('/complaint_management')
@jwt_required(locations=["cookies"])
def complaint_management():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    if role == 'user':
        return jsonify({"message": "No Permission"}), 401
    complaints = show_all_complaint_admin()
    return render_template("complaint_management.html", complaints = complaints)

'''
admin_response=123&complaint_name=123&complaint_product_name=Apple
admin resp, complaint user, complaint product
/admin_response
提交处理结果，更新到数据库中。
'''
@bp.route('/admin_response', methods = ["POST"])
@jwt_required(locations=["cookies"])
def complaint_management_admin():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    if role == 'user':
        return jsonify({"message": "No Permission"}), 401
    admin_resp = request.form['admin_response']
    complaint_user = request.form['complaint_name']
    complaint_product_name = request.form['complaint_product_name']
    res = update_complaint(complaint_user, complaint_product_name, admin_resp)
    if "error" in res:
        return jsonify({"message": "error"}), 500
    return jsonify({"message": "ok"}), 200

'''
/withdraw 下架产品

product_name=Apple
'''
@bp.route('/withdraw', methods = ['POST'])
@jwt_required(locations=["cookies"])
def withdraw():
    current_user = get_jwt_identity()
    role = get_jwt()['role']
    if role == 'user':
        return jsonify({"message": "No Permission"}), 401
    product_name = request.form['product_name']
    seller = request.form['seller']
    res = _withdraw(product_name, seller)
    if "error" in res:
        return jsonify({"message": "failed"}), 400
    return jsonify({"message": "ok"}), 200

