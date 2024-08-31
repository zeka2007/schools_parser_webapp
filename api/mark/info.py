from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_session
from db.mark import Mark
from .. import validate
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


mark_info_dp = APIRouter()


@mark_info_dp.get('/')
async def get_marks(
    diary_id: int,
    lesson_id: int,
    quarter: int,
    tg_data = Depends(validate.validate),
    session: AsyncSession = Depends(get_session)
):
    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == diary_id))
    diary = diary_result.scalars().first()

    lesson_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == lesson_id))
    lesson = lesson_result.scalars().first()

    marks_result = await session.execute(select(Mark).where(Mark.attached_to_lesson == lesson._id).where(Mark.quarter == quarter).order_by(Mark.date))
    marks = marks_result.scalars().all()

    data = []

    for m in marks:
        mark_dict = m.__dict__
        mark_dict.pop('_sa_instance_state')
        mark_dict['date'] = m.date.strftime('%Y-%m-%d')
        mark_dict.pop('quarter')
        data.append(mark_dict)    

    return data