"""患者端与医生调阅接口。"""
from flask import Blueprint, jsonify

from ..models import ROLE_PATIENT
from ..services import schedule_service
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
