from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.mark import Mark
from .. import validate
from db import get_session
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


lesson_info_dp = APIRouter()


@lesson_info_dp.get('/')
async def get_diary_info(
        diary_id: int,
        tg_data = Depends(validate.validate), 
        session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == diary_id))
    diary = diary_result.scalars().first()

    lessons_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary._id))
    lessons = lessons_result.scalars().all()

    data = []


    for l in lessons:
        marks_data_result = await session.execute(select(Mark).where(Mark.attached_to_lesson == l._id))
        marks_data = marks_data_result.scalars().all()
        marks = [[], [], [], []]

        for m in marks_data:
            mark_dict = m.__dict__
            mark_dict.pop('_sa_instance_state')
            mark_dict['date'] = m.date.strftime('%m-%d-%Y')
            marks[m.quarter - 1].append(mark_dict)
            mark_dict.pop('quarter')


        data.append({
                "id": l._id, 
                "name": l.name, 
                "attached_to_diary": l.attached_to_diary, 
                "marks": marks
            })
    
    return data