from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    # 参数校验
    errors = []
    if not username or len(username) < 2:
        errors.append("用户名至少 2 个字符")
    if not email or "@" not in email:
        errors.append("邮箱格式不正确")
    if not password or len(password) < 6:
        errors.append("密码至少 6 个字符")
    if errors:
        return jsonify({"error": "；".join(errors)}), 400

    # 唯一性检查
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "邮箱已注册"}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "注册成功", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """用户登录，返回 JWT Token"""
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "请输入用户名和密码"}), 400

    user = User.query.filter_by(username=data["username"].strip()).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "用户名或密码错误"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "user": user.to_dict()})


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    """获取当前登录用户信息"""
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    return jsonify({"user": user.to_dict()})
