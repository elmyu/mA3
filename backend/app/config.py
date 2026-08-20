"""应用配置。"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "minibmehub.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


def ensure_storage():
    """确保数据库与上传目录存在（SQLite 不会自动创建父目录/文件）。"""
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    open(DB_PATH, "a").close()


ensure_storage()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "minibmehub-dev-secret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "minibmehub-jwt-secret-key-for-dev-2026")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH.replace("\\", "/")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
