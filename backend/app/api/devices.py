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


@bp.post("")
@role_required(ROLE_ADMIN)
def create_device():
    """录入新设备（管理员）
    ---
    tags: [管理员端]
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [name]
          properties:
            name: {type: string}
            status: {type: string, enum: [online, fault, calibrating]}
            last_calibration_date: {type: string, example: "2026-08-01"}
            location: {type: string}
    responses:
      201:
        description: 创建成功
    """
    device = device_service.create_device(request.get_json(silent=True) or {})
    return jsonify({"code": 0, "data": device.to_dict()}), 201


@bp.put("/<int:device_id>")
@role_required(ROLE_ADMIN)
def update_device(device_id):
    """修改设备（管理员）
    ---
    tags: [管理员端]
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
          properties:
            name: {type: string}
            status: {type: string, enum: [online, fault, calibrating]}
            last_calibration_date: {type: string}
            location: {type: string}
    responses:
      200:
        description: 更新成功
    """
    device = device_service.update_device(device_id, request.get_json(silent=True) or {})
    return jsonify({"code": 0, "data": device.to_dict()})


@bp.delete("/<int:device_id>")
@role_required(ROLE_ADMIN)
def delete_device(device_id):
    """删除设备（管理员）
    ---
    tags: [管理员端]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: device_id
        required: true
        schema: {type: integer}
    responses:
      200:
        description: 删除成功
      400:
        description: 存在关联预约无法删除
    """
    device_service.delete_device(device_id)
    return jsonify({"code": 0, "message": "删除成功"})
