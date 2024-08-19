import datetime

from sqlalchemy import func, BigInteger, ARRAY, VARCHAR, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from . import database

class Lesson(database.Model):
    __tablename__ = "lessons"

    _id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
   
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False, unique=False)
    attached_to_diary: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=False)

    marks = mapped_column(JSONB, unique=False)


    def __str__(self) -> str:
        return f'<Lesson:{self._id}>'
