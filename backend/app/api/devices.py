"""设备台账与维护接口。"""
from flask import Blueprint, jsonify, request

from ..models import ROLE_ADMIN, ROLE_DOCTOR
from ..services import device_service
from ..utils.auth import role_required

bp = Blueprint("devices", __name__, url_prefix="/api/devices")


@bp.get("")
@role_required(ROLE_DOCTOR, ROLE_ADMIN)
def list_devices():
    """设备台账列表
    ---
    tags: [医生端]
    security:
      - Bearer: []
    responses:
      200:
        description: 全部医疗设备
    """
    devices = device_service.list_all()
    return jsonify({"code": 0, "data": [d.to_dict() for d in devices]})


@bp.put("/<int:device_id>/status")
@role_required(ROLE_DOCTOR, ROLE_ADMIN)
def update_status(device_id):
    """修改设备状态
    ---
    tags: [医生端]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: device_id
        required: true
        schema: {type: integer}
      - in: body
        name: body
        schema:
          type: object
          required: [status]
          properties:
            status: {type: string, enum: [online, fault, calibrating]}
    responses:
      200:
        description: 更新后的设备信息
    """
    data = request.get_json(silent=True) or {}
    device = device_service.update_status(device_id, data.get("status", ""))
    return jsonify({"code": 0, "data": device.to_dict()})
