import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.lesson import Lesson
from db.mark import Mark
from .. import validate
from db import get_session
from db.virtual_diary import VirtualDiary


delete_lesson_dp = APIRouter()

class DeleteLesson(BaseModel):
    id: int
    diary_id: int
    

@delete_lesson_dp.post('/')
async def delete_lesson(data: DeleteLesson, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == data.diary_id))
    diary = diary_result.scalars().first()

    await session.execute(delete(Lesson).where(Lesson._id == data.id).where(Lesson.attached_to_diary == diary._id))
    await session.execute(delete(Mark).where(Mark.attached_to_lesson == data.id))
    
    await session.commit()
