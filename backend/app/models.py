"""数据模型：用户、设备、生理信号记录、预约记录、医生排班。"""
import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ROLE_PATIENT = "patient"
ROLE_DOCTOR = "doctor"
ROLE_ADMIN = "admin"

DEVICE_ONLINE = "online"
DEVICE_FAULT = "fault"
DEVICE_CALIBRATING = "calibrating"

APPOINTMENT_BOOKED = "booked"
APPOINTMENT_COMPLETED = "completed"
APPOINTMENT_CANCELLED = "cancelled"

SCHEDULE_AVAILABLE = "available"
SCHEDULE_BUSY = "busy"


def _fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)
    real_name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)

    signal_records = db.relationship("SignalRecord", backref="patient", lazy=True)
    appointments = db.relationship(
        "Appointment", foreign_keys="Appointment.doctor_id", backref="doctor", lazy=True
    )
    schedules = db.relationship("DoctorSchedule", backref="doctor", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "real_name": self.real_name,
            "gender": self.gender,
            "age": self.age,
            "phone": self.phone,
            "created_at": _fmt(self.created_at),
        }


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=DEVICE_ONLINE, index=True)
    last_calibration_date = db.Column(db.Date)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

    appointments = db.relationship("Appointment", backref="device", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "last_calibration_date": (
                self.last_calibration_date.isoformat() if self.last_calibration_date else None
            ),
            "location": self.location,
            "created_at": _fmt(self.created_at),
        }


class SignalRecord(db.Model):
    __tablename__ = "signal_records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    signal_type = db.Column(db.String(50), nullable=False)
    sample_rate = db.Column(db.Integer, nullable=False, default=250)
    data_json = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255))
    recorded_at = db.Column(db.DateTime, default=datetime.now, index=True)

    def values(self):
        try:
            return json.loads(self.data_json or "[]")
        except ValueError:
            return []

    def to_dict(self, include_values=False):
        data = {
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_name": (
                self.patient.real_name or self.patient.username if self.patient else None
            ),
            "signal_type": self.signal_type,
            "sample_rate": self.sample_rate,
            "file_path": self.file_path,
            "recorded_at": _fmt(self.recorded_at),
        }
        if include_values:
            data["values"] = self.values()
        return data


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=APPOINTMENT_BOOKED)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_name": self.device.name if self.device else None,
            "doctor_id": self.doctor_id,
            "doctor_name": (
                self.doctor.real_name or self.doctor.username if self.doctor else None
            ),
            "start_time": _fmt(self.start_time),
            "end_time": _fmt(self.end_time),
            "status": self.status,
            "created_at": _fmt(self.created_at),
        }


class DoctorSchedule(db.Model):
    __tablename__ = "doctor_schedules"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    schedule_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=SCHEDULE_AVAILABLE)

    def to_dict(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "doctor_name": (
                self.doctor.real_name or self.doctor.username if self.doctor else None
            ),
            "schedule_date": (
                self.schedule_date.isoformat() if self.schedule_date else None
            ),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
        }
