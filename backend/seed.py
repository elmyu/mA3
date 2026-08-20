"""初始化数据库：建表并写入演示数据（可重复运行）。"""
import json
import math
import random
from datetime import date, datetime, timedelta

from werkzeug.security import generate_password_hash

from app import create_app
from app.models import (
    APPOINTMENT_BOOKED,
    DEVICE_CALIBRATING,
    DEVICE_FAULT,
    DEVICE_ONLINE,
    SCHEDULE_AVAILABLE,
    Appointment,
    Device,
    DoctorSchedule,
    SignalRecord,
    User,
    db,
)

app = create_app()


def gen_ecg(seconds=10, sample_rate=250):
    """生成一段模拟 ECG 波形数值。"""
    random.seed(42)
    values = []
    for i in range(seconds * sample_rate):
        t = i / sample_rate
        phase = (t % 0.8) / 0.8
        qrs = math.exp(-((phase - 0.18) ** 2) / 0.0015)
        t_wave = 0.18 * math.exp(-((phase - 0.55) ** 2) / 0.008)
        values.append(
            round(
                0.05 * math.sin(2 * math.pi * 1.2 * t)
                + qrs
                + t_wave
                + random.uniform(-0.02, 0.02),
                4,
            )
        )
    return values


def seed():
    with app.app_context():
        db.create_all()
        if User.query.first() is not None:
            print("数据库已有数据，跳过种子初始化。")
            return

        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin",
            real_name="系统管理员",
        )
        doctor = User(
            username="doctor1",
            password_hash=generate_password_hash("123456"),
            role="doctor",
            real_name="王医生",
            gender="男",
            age=42,
            phone="13800000001",
        )
        patient = User(
            username="patient1",
            password_hash=generate_password_hash("123456"),
            role="patient",
            real_name="李小明",
            gender="男",
            age=28,
            phone="13800000002",
        )
        db.session.add_all([admin, doctor, patient])
        db.session.flush()

        devices = [
            Device(
                name="多参数监护仪 A1",
                status=DEVICE_ONLINE,
                last_calibration_date=date(2026, 5, 20),
                location="重症监护室",
            ),
            Device(
                name="超声诊断仪 U2",
                status=DEVICE_ONLINE,
                last_calibration_date=date(2026, 6, 1),
                location="超声科",
            ),
            Device(
                name="心电图机 E3",
                status=DEVICE_FAULT,
                last_calibration_date=date(2026, 3, 15),
                location="心内科",
            ),
            Device(
                name="呼吸机 R4",
                status=DEVICE_CALIBRATING,
                last_calibration_date=date(2026, 7, 10),
                location="呼吸科",
            ),
            Device(
                name="血糖仪 G5",
                status=DEVICE_ONLINE,
                last_calibration_date=date(2026, 8, 1),
                location="门诊",
            ),
        ]
        db.session.add_all(devices)
        db.session.flush()

        db.session.add_all(
            [
                SignalRecord(
                    patient_id=patient.id,
                    signal_type="ECG",
                    sample_rate=250,
                    data_json=json.dumps(gen_ecg()),
                    recorded_at=datetime.now() - timedelta(days=2),
                ),
                SignalRecord(
                    patient_id=patient.id,
                    signal_type="ECG",
                    sample_rate=250,
                    data_json=json.dumps(gen_ecg()),
                    recorded_at=datetime.now() - timedelta(days=1),
                ),
            ]
        )

        today = date.today()
        db.session.add_all(
            [
                DoctorSchedule(
                    doctor_id=doctor.id,
                    schedule_date=today + timedelta(days=1),
                    start_time="08:30",
                    end_time="12:00",
                    status=SCHEDULE_AVAILABLE,
                ),
                DoctorSchedule(
                    doctor_id=doctor.id,
                    schedule_date=today + timedelta(days=1),
                    start_time="14:00",
                    end_time="17:30",
                    status=SCHEDULE_AVAILABLE,
                ),
                DoctorSchedule(
                    doctor_id=doctor.id,
                    schedule_date=today + timedelta(days=3),
                    start_time="09:00",
                    end_time="11:30",
                    status=SCHEDULE_AVAILABLE,
                ),
            ]
        )

        db.session.add(
            Appointment(
                device_id=devices[0].id,
                doctor_id=doctor.id,
                start_time=datetime.now() + timedelta(hours=3),
                end_time=datetime.now() + timedelta(hours=4),
                status=APPOINTMENT_BOOKED,
            )
        )
        db.session.commit()
        print("演示数据初始化完成。账号：admin/admin123、doctor1/123456、patient1/123456")


if __name__ == "__main__":
    seed()
