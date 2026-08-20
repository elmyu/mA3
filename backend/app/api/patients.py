"""患者端与医生调阅接口。"""
from flask import Blueprint, jsonify

from ..models import ROLE_ADMIN, ROLE_DOCTOR, ROLE_PATIENT
from ..services import patient_service, schedule_service, signal_service
from ..utils.auth import role_required

bp = Blueprint("patients", __name__, url_prefix="/api")


@bp.get("/doctors/schedules")
@role_required(ROLE_PATIENT)
def doctor_schedules():
    """医生出诊/空闲时间表
    ---
    tags: [患者端]
    security:
      - Bearer: []
    responses:
      200:
        description: 医生空闲排班列表
    """
    schedules = schedule_service.list_available()
    return jsonify({"code": 0, "data": [s.to_dict() for s in schedules]})


@bp.get("/patients")
@role_required(ROLE_DOCTOR, ROLE_ADMIN)
def list_patients():
    """患者列表（医生调阅）
    ---
    tags: [医生端]
    security:
      - Bearer: []
    responses:
      200:
        description: 全部患者及基本信息
    """
    patients = patient_service.list_patients()
    return jsonify({"code": 0, "data": [p.to_dict() for p in patients]})


@bp.get("/patients/<int:patient_id>/signals")
@role_required(ROLE_DOCTOR, ROLE_ADMIN)
def patient_signals(patient_id):
    """查看某患者的信号记录（医生调阅）
    ---
    tags: [医生端]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: patient_id
        required: true
        schema: {type: integer}
    responses:
      200:
        description: 患者信息及其信号记录
      404:
        description: 患者不存在
    """
    patient = patient_service.get_patient(patient_id)
    records = signal_service.list_by_patient(patient.id)
    return jsonify(
        {
            "code": 0,
            "data": {
                "patient": patient.to_dict(),
                "records": [r.to_dict() for r in records],
            },
        }
    )
