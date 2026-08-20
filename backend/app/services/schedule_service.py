"""医生排班业务逻辑。"""
from ..models import SCHEDULE_AVAILABLE, DoctorSchedule


def list_available():
    return DoctorSchedule.query.filter_by(status=SCHEDULE_AVAILABLE).order_by(
        DoctorSchedule.schedule_date, DoctorSchedule.start_time
    )
