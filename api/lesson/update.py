import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .. import validate
from db import get_session
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


update_lesson_dp = APIRouter()

class UpdateLesson(BaseModel):
    id: int
    attached_to: int
    fields: dict

@update_lesson_dp.post('/')
async def update_lesson(data: UpdateLesson, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary._id == data['attached_to']).where(VirtualDiary.attached_to == user_id))
    diary = diary_result.scalars().first()

    await session.execute(update(Lesson).where(Lesson._id == data['id']).where(Lesson.attached_to_diary == diary._id).values(**data.fields))
        
    await session.commit()
