"""设备预约接口。"""
from flask import Blueprint, g, jsonify, request

from ..models import ROLE_DOCTOR
from ..services import appointment_service
from ..utils.auth import role_required

bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")


@bp.post("")
@role_required(ROLE_DOCTOR)
def create_appointment():
    """创建设备预约
    ---
    tags: [医生端]
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [device_id, start_time, end_time]
          properties:
            device_id: {type: integer}
            start_time: {type: string, example: "2026-08-21 10:00:00"}
            end_time: {type: string, example: "2026-08-21 11:00:00"}
    responses:
      201:
        description: 预约成功
      400:
        description: 设备不可预约或时间不合法
      409:
        description: 时间段冲突
    """
    data = request.get_json(silent=True) or {}
    appointment = appointment_service.create_appointment(
        g.current_user.id,
        data.get("device_id"),
        data.get("start_time"),
        data.get("end_time"),
    )
    return jsonify({"code": 0, "data": appointment.to_dict()}), 201


@bp.get("")
@role_required(ROLE_DOCTOR)
def list_my_appointments():
    """我的预约列表
    ---
    tags: [医生端]
    security:
      - Bearer: []
    responses:
      200:
        description: 当前医生的预约记录
    """
    appointments = appointment_service.list_by_doctor(g.current_user.id)
    return jsonify({"code": 0, "data": [a.to_dict() for a in appointments]})
