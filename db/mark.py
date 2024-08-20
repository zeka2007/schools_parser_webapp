import datetime

from sqlalchemy import Date, func, BigInteger, VARCHAR, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from . import database

class Mark(database.Model):
    __tablename__ = "marks"

    _id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
   
    first_value: Mapped[int] = mapped_column(Integer, nullable=True, unique=False)
    second_value: Mapped[int] = mapped_column(Integer, nullable=True, unique=False)
    display_value: Mapped[str] = mapped_column(VARCHAR, nullable=True, unique=False)

    date: Mapped[datetime.datetime] = mapped_column(Date, nullable=False, unique=False)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)


    attached_to_lesson: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=False)


    def __str__(self) -> str:
        return f'<Mark:{self._id}>'
