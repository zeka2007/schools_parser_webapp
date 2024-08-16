import datetime

from sqlalchemy import func, BigInteger, ARRAY, VARCHAR, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from . import database

class Student(database.Model):
    __tablename__ = "students"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
   
    reg_date: Mapped[datetime.datetime] = mapped_column(unique=False, nullable=True, server_default=func.now())

    # Student settings
    full_view_model: Mapped[bool] = mapped_column(Boolean, unique=False, default=False)

    admin_level: Mapped[int] = Column(Integer, unique=False, nullable=False, default=0)
    is_sponsor: Mapped[bool] = mapped_column(Boolean, unique=False, default=False)

    newsletters_alarm_state: Mapped[bool] = mapped_column(Boolean, unique=False, default=False)

    def __str__(self) -> str:
        return f'<Student:{self.user_id}>'
