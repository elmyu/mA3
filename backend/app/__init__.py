"""Flask 应用工厂。"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from .config import Config
from .errors import ApiError
from .models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    Swagger(
        app,
        template={
            "info": {
                "title": "Mini BME-Hub API",
                "description": "医疗设备管理平台接口文档",
                "version": "1.0.0",
            },
            "securityDefinitions": {
                "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
            },
        },
    )

    from .api import register_blueprints

    register_blueprints(app)

    @app.errorhandler(ApiError)
    def handle_api_error(err):
        return jsonify({"code": err.code, "message": err.message}), err.code

    @app.errorhandler(413)
    def handle_too_large(_err):
        return jsonify({"code": 413, "message": "文件过大，最大 10MB"}), 413

    return app
