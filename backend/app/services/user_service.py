"""用户管理业务逻辑。"""
from werkzeug.security import generate_password_hash

from ..errors import ApiError
from ..models import ROLE_ADMIN, ROLE_DOCTOR, ROLE_PATIENT, User, db

ROLES = (ROLE_PATIENT, ROLE_DOCTOR, ROLE_ADMIN)


def list_users():
    return User.query.order_by(User.id)


def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise ApiError("用户不存在", 404)
    return user


def create_user(data):
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    role = data.get("role")
    if not username or not password or role not in ROLES:
        raise ApiError("用户名、密码与角色不能为空且角色必须合法", 400)
    if User.query.filter_by(username=username).first() is not None:
        raise ApiError("用户名已存在", 409)
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role,
        real_name=data.get("real_name"),
        gender=data.get("gender"),
        age=data.get("age"),
        phone=data.get("phone"),
    )
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user_id, data):
    user = get_user(user_id)
    if "username" in data:
        username = (data.get("username") or "").strip()
        if not username:
            raise ApiError("用户名不能为空", 400)
        exists = User.query.filter(User.username == username, User.id != user_id).first()
        if exists is not None:
            raise ApiError("用户名已存在", 409)
        user.username = username
    password = data.get("password")
    if password:
        user.password_hash = generate_password_hash(password)
    if "role" in data and data["role"] not in ROLES:
        raise ApiError("角色必须合法", 400)
    user.role = data.get("role", user.role)
    for field in ("real_name", "gender", "age", "phone"):
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return user


def delete_user(user_id, current_user):
    user = get_user(user_id)
    if user.id == current_user.id:
        raise ApiError("不能删除当前登录账号", 400)
    if user.signal_records or user.appointments or user.schedules:
        raise ApiError("该用户存在关联数据，无法删除", 400)
    db.session.delete(user)
    db.session.commit()
