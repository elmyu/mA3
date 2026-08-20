"""用户管理接口（管理员）。"""
from flask import Blueprint, g, jsonify, request

from ..models import ROLE_ADMIN
from ..services import user_service
from ..utils.auth import role_required

bp = Blueprint("users", __name__, url_prefix="/api/users")


@bp.get("")
@role_required(ROLE_ADMIN)
def list_users():
    """用户列表
    ---
    tags: [管理员端]
    security:
      - Bearer: []
    responses:
      200:
        description: 全部用户
    """
    users = user_service.list_users()
    return jsonify({"code": 0, "data": [u.to_dict() for u in users]})


@bp.post("")
@role_required(ROLE_ADMIN)
def create_user():
    """新增用户
    ---
    tags: [管理员端]
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [username, password, role]
          properties:
            username: {type: string}
            password: {type: string}
            role: {type: string, enum: [patient, doctor, admin]}
            real_name: {type: string}
            gender: {type: string}
            age: {type: integer}
            phone: {type: string}
    responses:
      201:
        description: 创建成功
      409:
        description: 用户名已存在
    """
    user = user_service.create_user(request.get_json(silent=True) or {})
    return jsonify({"code": 0, "data": user.to_dict()}), 201


@bp.put("/<int:user_id>")
@role_required(ROLE_ADMIN)
def update_user(user_id):
    """修改用户
    ---
    tags: [管理员端]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        required: true
        schema: {type: integer}
      - in: body
        name: body
        schema:
          type: object
          properties:
            username: {type: string}
            password: {type: string}
            role: {type: string, enum: [patient, doctor, admin]}
    responses:
      200:
        description: 更新成功
    """
    user = user_service.update_user(user_id, request.get_json(silent=True) or {})
    return jsonify({"code": 0, "data": user.to_dict()})


@bp.delete("/<int:user_id>")
@role_required(ROLE_ADMIN)
def delete_user(user_id):
    """删除用户
    ---
    tags: [管理员端]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        required: true
        schema: {type: integer}
    responses:
      200:
        description: 删除成功
      400:
        description: 不能删除当前账号或存在关联数据
    """
    user_service.delete_user(user_id, g.current_user)
    return jsonify({"code": 0, "message": "删除成功"})
