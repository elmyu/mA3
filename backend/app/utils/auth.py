"""鉴权工具：JWT 身份注入与角色校验。"""
from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..models import User


def role_required(*roles):
    """校验 JWT，限制访问角色，并把当前用户注入 flask.g。"""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.get(int(get_jwt_identity()))
            if user is None:
                return jsonify({"code": 401, "message": "用户不存在或已失效"}), 401
            if roles and user.role not in roles:
                return jsonify({"code": 403, "message": "无权限访问"}), 403
            g.current_user = user
            return fn(*args, **kwargs)

        return wrapper

    return decorator
