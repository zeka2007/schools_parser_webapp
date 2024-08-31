from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db.mark import Mark
from .. import validate
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


create_mark_dp = APIRouter()

class CreateMark(BaseModel):
    first_value: int | None
    second_value: int | None
    display_value: str | None
    quarter: int
    diary_id: int
    attached_to_lesson: int
    date: str

@create_mark_dp.post('/')
async def create_mark(data: CreateMark, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):

    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary._id == data.diary_id).where(VirtualDiary.attached_to == user_id))
    diary = diary_result.scalars().first()

    lesson_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == data.attached_to_lesson))
    lesson = lesson_result.scalars().first()

    if lesson is None: raise HTTPException(status_code=404)

    data.__dict__.pop('diary_id')
    data.date = datetime.strptime(data.date, "%Y-%m-%d")

    mark = Mark(**data.__dict__)
    session.add(mark)

    await session.commit()
    await session.flush()
    await session.refresh(mark)

    return {'id': mark._id}