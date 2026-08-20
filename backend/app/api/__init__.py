"""API 蓝图注册。"""


def register_blueprints(app):
    from . import appointments, auth, devices, patients, signals

    for blueprint in (auth.bp, patients.bp, signals.bp, devices.bp, appointments.bp):
        app.register_blueprint(blueprint)
