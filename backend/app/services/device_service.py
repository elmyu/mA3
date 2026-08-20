"""设备业务逻辑。"""
from ..errors import ApiError
from ..models import DEVICE_CALIBRATING, DEVICE_FAULT, DEVICE_ONLINE, Device, db

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
