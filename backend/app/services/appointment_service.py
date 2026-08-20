"""预约业务逻辑。"""
from datetime import datetime

from ..errors import ApiError
from ..models import (
    APPOINTMENT_BOOKED,
    DEVICE_ONLINE,
    Appointment,
    Device,
    db,
)


def _parse_time(value):
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        raise ApiError("时间格式应为 YYYY-MM-DD HH:MM:SS", 400)


def create_appointment(doctor_id, device_id, start_time, end_time):
    start = _parse_time(start_time)
    end = _parse_time(end_time)
    if end <= start:
        raise ApiError("结束时间必须晚于开始时间", 400)

    device = Device.query.get(device_id)
    if device is None:
        raise ApiError("设备不存在", 404)
    if device.status != DEVICE_ONLINE:
        raise ApiError("设备当前不可预约", 400)

    conflict = Appointment.query.filter(
        Appointment.device_id == device_id,
        Appointment.status == APPOINTMENT_BOOKED,
        Appointment.start_time < end,
        Appointment.end_time > start,
    ).first()
    if conflict is not None:
        raise ApiError("该设备在此时间段已被预约", 409)

    appointment = Appointment(
        device_id=device_id,
        doctor_id=doctor_id,
        start_time=start,
        end_time=end,
        status=APPOINTMENT_BOOKED,
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment


def list_by_doctor(doctor_id):
    return Appointment.query.filter_by(doctor_id=doctor_id).order_by(
        Appointment.start_time.desc()
    )
