from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from db.lesson import Lesson
from db.mark import Mark
from .. import validate
from db import get_session
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_marks_dp = APIRouter()

class DeleteMark(BaseModel):
    diary_id: int
    lesson_id: int
    mark_ids: List[int] = None


@delete_marks_dp.post('/')
async def delete_mark(data: DeleteMark, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']


    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == data.diary_id))
    diary = diary_result.scalars().first()
    lesson_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == data.lesson_id))
    lesson = lesson_result.scalars().first()

    delete_query = delete(Mark).where(Mark.attached_to_lesson == lesson._id)

    if data.mark_ids is not None:
        delete_query = delete_query.where(Mark._id.in_(tuple(data.mark_ids)))

    await session.execute(delete_query)
    await session.commit()
