import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from .. import validate
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


create_lesson_dp = APIRouter()


class CreateLesson(BaseModel):
    diary_id: int
    name: str

@create_lesson_dp.post('/')
async def create_lesson(data: CreateLesson, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary._id == data.diary_id).where(VirtualDiary.attached_to == user_id))
    diary = diary_result.scalars().first()

    db_lessons_count_result = await session.execute(select(func.count(Lesson._id)).where(Lesson.attached_to_diary == diary._id).where(Lesson.name == data.name))

    if db_lessons_count_result.scalar() != 0:
        raise HTTPException(status_code=409)

    lesson: Lesson = Lesson(
        name=data.name,
        attached_to_diary=diary._id
    )

    session.add(lesson)
    
    await session.commit()
    await session.flush()
    await session.refresh(lesson)

    return {'id': lesson._id}