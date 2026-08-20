"""API 蓝图注册。"""


def register_blueprints(app):
    from . import appointments, auth, devices, patients, signals, users

    for blueprint in (
        auth.bp,
        patients.bp,
        signals.bp,
        devices.bp,
        appointments.bp,
        users.bp,
    ):
        app.register_blueprint(blueprint)
