"""API 蓝图注册。"""


def register_blueprints(app):
    from . import auth, patients, signals

    for blueprint in (auth.bp, patients.bp, signals.bp):
        app.register_blueprint(blueprint)
