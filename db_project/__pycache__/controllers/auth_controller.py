from flask import Flask, request, jsonify, render_template, Blueprint,url_for,redirect, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from utils.db import get_db_connection, register_user, login_user
import re

# 实现用户的注册和登录路由

bp = Blueprint('auth', __name__)

def validate_username(username):
    return re.match("^[a-zA-Z0-9_]+$", username) is not None

def validate_password(password):
    return re.match("^[a-zA-Z0-9@#$%^&+=!]{8,}$", password) is not None


@bp.route('/', methods = ['GET', 'POST'])
def index():
    return redirect('/register')
@bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not validate_username(username):
            return jsonify({"error": "用户名限制为字母、数字和下划线"}), 400
        if not validate_password(password):
            return jsonify({"error": "密码限制为字母、数字和特殊符号，且长度至少为8"}), 400
        if len(username) > 50:
            return jsonify({"error": "用户名长度过长"}), 400
        result = register_user(username, password)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    else:
        return render_template('register.html')

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not validate_username(username):
            return jsonify({"error": "用户名限制为字母、数字和下划线"}), 400
        if not validate_password(password):
            return jsonify({"error": "密码限制为字母、数字和特殊符号，且长度至少为8"}), 400
        user = login_user(username, password)
        if user:
            if user['is_banned'] == "true":
                return jsonify({"error": "该用户已被冻结"}), 400
            token = create_access_token(identity=user['username'], additional_claims={"role": user['role'], "is_banned": user['is_banned']})
            response = jsonify({"message": "登录成功"})
            set_access_cookies(response, token)
            return response, 200
        else:
            return jsonify({"error":"用户名或密码错误"}), 401
    else:
        return render_template('login.html')