"""生理信号业务逻辑。"""
from ..errors import ApiError
from ..models import ROLE_PATIENT, SignalRecord


def list_own(user_id):
    return SignalRecord.query.filter_by(patient_id=user_id).order_by(SignalRecord.recorded_at.desc())


def list_by_patient(patient_id):
    return SignalRecord.query.filter_by(patient_id=patient_id).order_by(
        SignalRecord.recorded_at.desc()
    )


def get_accessible_record(record_id, user):
    record = SignalRecord.query.get(record_id)
    if record is None:
        raise ApiError("记录不存在", 404)
    if user.role == ROLE_PATIENT and record.patient_id != user.id:
        raise ApiError("无权限访问", 403)
    return record
