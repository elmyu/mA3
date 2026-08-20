"""CSV 生理数据上传业务逻辑。"""
import csv
import io
import json
import os
import uuid

from flask import current_app

from ..errors import ApiError
from ..models import ROLE_DOCTOR, SignalRecord, db


def _parse_values(raw):
    text = raw.decode("utf-8-sig", errors="replace")
    values = []
    for row in csv.reader(io.StringIO(text)):
        for cell in row:
            try:
                values.append(float(cell.strip()))
            except (ValueError, AttributeError):
                continue
    if not values:
        raise ApiError("CSV 中未找到有效的数值数据", 400)
    return values


def save_csv(file_storage, user, signal_type, sample_rate, patient_id=None):
    if file_storage is None or not file_storage.filename:
        raise ApiError("请选择要上传的 CSV 文件", 400)
    if not file_storage.filename.lower().endswith(".csv"):
        raise ApiError("仅支持 .csv 文件", 400)

    owner_id = user.id if user.role != ROLE_DOCTOR else patient_id
    if owner_id is None:
        raise ApiError("医生上传时必须指定患者 patient_id", 400)

    raw = file_storage.read()
    if len(raw) > current_app.config["MAX_CONTENT_LENGTH"]:
        raise ApiError("文件过大，最大 10MB", 400)
    values = _parse_values(raw)

    filename = f"{user.id}_{uuid.uuid4().hex[:8]}.csv"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    file_path = "uploads/" + filename
    with open(os.path.join(folder, filename), "wb") as f:
        f.write(raw)

    record = SignalRecord(
        patient_id=int(owner_id),
        signal_type=(signal_type or "ECG").strip() or "ECG",
        sample_rate=int(sample_rate or 250),
        data_json=json.dumps(values),
        file_path=file_path,
    )
    db.session.add(record)
    db.session.commit()
    return record
