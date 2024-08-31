from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.lesson import Lesson
from db.mark import Mark
from db.student import Student
from .. import validate
from db import get_session
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_student_dp = APIRouter()


@delete_student_dp.post('/')
async def delete_user(tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    v_diaries_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id))
    v_diaries = v_diaries_result.scalars().all()

    for v_diary in v_diaries:
        lessons_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == v_diary._id))
        lessons = lessons_result.scalars().all()

        for lesson in lessons:
            await session.execute(delete(Mark).where(Mark.attached_to_lesson == lesson._id))
        await session.execute(delete(Lesson).where(Lesson.attached_to_diary == v_diary._id))

    await session.execute(delete(VirtualDiary).where(VirtualDiary.attached_to == user_id))
    await session.execute(delete(Diary).where(Diary.attached_to == user_id))
    await session.execute(delete(Student).where(Student.user_id == user_id))

    await session.commit()
