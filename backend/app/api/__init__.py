"""API 蓝图注册。"""


def register_blueprints(app):
    from . import auth

    app.register_blueprint(auth.bp)
