"""生理信号接口。"""
from flask import Blueprint, g, jsonify, request

from ..models import ROLE_DOCTOR, ROLE_PATIENT
from ..services import signal_service, upload_service
from ..utils.auth import role_required

bp = Blueprint("signals", __name__, url_prefix="/api/signals")


@bp.get("/my")
@role_required(ROLE_PATIENT)
def my_signals():
    """我的生理信号记录
    ---
    tags: [患者端]
    security:
      - Bearer: []
    responses:
      200:
        description: 当前患者本人的信号记录列表
      403:
        description: 非患者角色无权限
    """
    records = signal_service.list_own(g.current_user.id)
    return jsonify({"code": 0, "data": [r.to_dict() for r in records]})


@bp.get("/<int:record_id>/waveform")
@role_required(ROLE_PATIENT, ROLE_DOCTOR)
def waveform(record_id):
    """获取信号波形数据（患者本人或医生）
    ---
    tags: [患者端]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: record_id
        required: true
        schema: {type: integer}
    responses:
      200:
        description: 波形数值数组
      403:
        description: 患者无权查看他人记录
    """
    record = signal_service.get_accessible_record(record_id, g.current_user)
    return jsonify(
        {
            "code": 0,
            "data": {
                "id": record.id,
                "signal_type": record.signal_type,
                "sample_rate": record.sample_rate,
                "values": record.values(),
            },
        }
    )


@bp.post("/upload")
@role_required(ROLE_PATIENT, ROLE_DOCTOR)
def upload():
    """上传生理数据 CSV 文件
    ---
    tags: [患者端]
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
      - in: formData
        name: signal_type
        type: string
      - in: formData
        name: sample_rate
        type: integer
      - in: formData
        name: patient_id
        type: integer
    responses:
      201:
        description: 上传成功并生成信号记录
      400:
        description: 文件类型或内容不合法
    """
    form = request.form
    record = upload_service.save_csv(
        request.files.get("file"),
        g.current_user,
        form.get("signal_type"),
        form.get("sample_rate"),
        form.get("patient_id"),
    )
    return jsonify({"code": 0, "data": record.to_dict()}), 201
