"""设备业务逻辑。"""
from datetime import date

from ..errors import ApiError
from ..models import (
    DEVICE_CALIBRATING,
    DEVICE_FAULT,
    DEVICE_ONLINE,
    Appointment,
    Device,
    db,
)

DEVICE_STATUSES = (DEVICE_ONLINE, DEVICE_FAULT, DEVICE_CALIBRATING)


def list_all():
    return Device.query.order_by(Device.id)


def get_device(device_id):
    device = Device.query.get(device_id)
    if device is None:
        raise ApiError("设备不存在", 404)
    return device


def update_status(device_id, status):
    if status not in DEVICE_STATUSES:
        raise ApiError("无效的设备状态", 400)
    device = get_device(device_id)
    device.status = status
    db.session.commit()
    return device


def _parse_date(value):
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ApiError("日期格式应为 YYYY-MM-DD", 400)


def create_device(data):
    name = (data.get("name") or "").strip()
    status = data.get("status") or DEVICE_ONLINE
    if not name:
        raise ApiError("设备名称不能为空", 400)
    if status not in DEVICE_STATUSES:
        raise ApiError("无效的设备状态", 400)
    device = Device(
        name=name,
        status=status,
        last_calibration_date=_parse_date(data.get("last_calibration_date")),
        location=data.get("location"),
    )
    db.session.add(device)
    db.session.commit()
    return device


def update_device(device_id, data):
    device = get_device(device_id)
    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            raise ApiError("设备名称不能为空", 400)
        device.name = name
    if "status" in data:
        if data["status"] not in DEVICE_STATUSES:
            raise ApiError("无效的设备状态", 400)
        device.status = data["status"]
    if "last_calibration_date" in data:
        device.last_calibration_date = _parse_date(data["last_calibration_date"])
    if "location" in data:
        device.location = data["location"]
    db.session.commit()
    return device


def delete_device(device_id):
    device = get_device(device_id)
    if Appointment.query.filter_by(device_id=device_id).first() is not None:
        raise ApiError("该设备存在关联预约，无法删除", 400)
    db.session.delete(device)
    db.session.commit()
