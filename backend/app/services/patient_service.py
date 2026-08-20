"""患者信息业务逻辑。"""
from ..errors import ApiError
from ..models import ROLE_PATIENT, User


def list_patients():
    return User.query.filter_by(role=ROLE_PATIENT).order_by(User.id)


def get_patient(patient_id):
    patient = User.query.get(patient_id)
    if patient is None or patient.role != ROLE_PATIENT:
        raise ApiError("患者不存在", 404)
    return patient
