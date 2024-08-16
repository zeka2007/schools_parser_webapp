from sqlalchemy import func, BigInteger, ARRAY, VARCHAR, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from Schoolsby_api.Schools_by import Student as WebStudent

from . import database

class Diary(database.Model):
    __tablename__ = "diaries"

    _id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
    attached_to = mapped_column(BigInteger, unique=False, nullable=False)

    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    login: Mapped[str] = mapped_column(unique=False, nullable=True)
    password: Mapped[str] = mapped_column(unique=False, nullable=True)
    csrf_token: Mapped[str] = mapped_column(unique=False, nullable=True)
    session_id: Mapped[str] = mapped_column(unique=False, nullable=True)
    student_id: Mapped[int] = mapped_column(unique=False, nullable=True)

    site_prefix: Mapped[str] = mapped_column(unique=False, nullable=True)
    
    # Alarm settings
    alarm_state: Mapped[bool] = mapped_column(Boolean, unique=False, default=False)
    alarm_lessons = Column(ARRAY(VARCHAR), unique=False, default=['*'])
    
    def __str__(self) -> str:
        return f'<diary:{self._id}>'

def get_schoolsby_student(diary: Diary) -> WebStudent:
    return WebStudent(
            diary.login,
            diary.password,
            diary.csrf_token,
            diary.session_id,
            diary.site_prefix,
            diary.student_id
        )