
from sqlalchemy import func, BigInteger, ARRAY, VARCHAR, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from . import database


class VirtualDiary(database.Model):
    __tablename__ = "virtual_diaries"

    _id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
    attached_to = mapped_column(BigInteger, unique=False, nullable=False)

    name: Mapped[str] = mapped_column(VARCHAR, nullable=False, unique=False)
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    lessons_ids = Column(ARRAY(BigInteger), unique=False, nullable=True)
    
    def __str__(self) -> str:
        return f'<diary:{self._id}>'
