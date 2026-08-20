"""认证接口。"""
from flask import Blueprint, g, jsonify, request
from flask_jwt_extended import create_access_token

from ..services import auth_service
from ..utils.auth import role_required

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    """登录
    ---
    tags: [认证]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [username, password]
          properties:
            username: {type: string}
            password: {type: string}
    responses:
      200:
        description: 登录成功，返回令牌与用户信息
      401:
        description: 用户名或密码错误
    """
    data = request.get_json(silent=True) or {}
    user = auth_service.authenticate(data.get("username", ""), data.get("password", ""))
    token = create_access_token(identity=str(user.id))
    return jsonify({"code": 0, "data": {"token": token, "user": user.to_dict()}})


@bp.get("/me")
@role_required()
def me():
    """获取当前登录用户信息
    ---
    tags: [认证]
    security:
      - Bearer: []
    responses:
      200:
        description: 当前用户信息
      401:
        description: 未登录或令牌失效
    """
    return jsonify({"code": 0, "data": g.current_user.to_dict()})
