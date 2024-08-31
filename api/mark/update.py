from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db.mark import Mark
from .. import validate
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


update_mark_dp = APIRouter()

class UpdateMark(BaseModel):
    id: int
    data: dict

@update_mark_dp.post('/')
async def update_mark(upd_date: UpdateMark, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    data = upd_date.data
    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary._id == data['diary_id']).where(VirtualDiary.attached_to == user_id))
    diary = diary_result.scalars().first()

    lesson_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == data['attached_to_lesson']))
    lesson = lesson_result.scalars().first()

    data.pop('diary_id')
    data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")

    await session.execute(update(Mark).where(Mark.attached_to_lesson == lesson._id).where(Mark._id == upd_date.id).values(**data))

    await session.commit()
   