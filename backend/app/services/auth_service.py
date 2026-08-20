"""认证业务逻辑。"""
from werkzeug.security import check_password_hash

from ..errors import ApiError
from ..models import User


def authenticate(username, password):
    user = User.query.filter_by(username=str(username or "")).first()
    if user is None or not check_password_hash(user.password_hash, str(password or "")):
        raise ApiError("用户名或密码错误", 401)
    return user
