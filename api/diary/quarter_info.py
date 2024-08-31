from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark
from db.lesson import Lesson
from .consts import SCHOOLS_BY_DIARY_INT, VIRTUAL_DIARY_INT
from db import get_session
from .. import validate
from db.virtual_diary import VirtualDiary
from db.diary import Diary, get_schoolsby_student
from db.mark import Mark as DBMark


quarter_info_dp = APIRouter()


@quarter_info_dp.get('/')
async def get_quarter_info(
        type: int = None,
        diary_id: int = None,
        quarter: int = None,
        tg_data = Depends(validate.validate),
        session: AsyncSession = Depends(get_session)):

    user_id = tg_data['user']['id']
    data = []

    if type == SCHOOLS_BY_DIARY_INT:
        diary_result = await session.execute(select(Diary).where(Diary.attached_to == user_id).where(Diary._id == diary_id))
        diary = diary_result.scalars().first()

        web_user = get_schoolsby_student(diary)
        marks: List[Mark] = await Schools_by.MarksManager.get_quarters_marks(web_user, int(quarter))
        for mark in marks:
            data.append(
                {
                    'lesson_name': mark.lesson.full_name,
                    'mark': 'Нет' if mark.value is None else mark.value
                }
            )
    elif type == VIRTUAL_DIARY_INT:
        diary_id_result = await session.execute(select(VirtualDiary._id).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == diary_id))
        diary_id = diary_id_result.scalar()

        lessons_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary_id))
        lessons = lessons_result.scalars().all()
        for lesson in lessons:
            db_marks_result = await session.execute(select(DBMark).where(DBMark.attached_to_lesson == lesson._id).where(DBMark.quarter == quarter))
            db_marks = db_marks_result.scalars().all()
            marks_list = []

            for mark in db_marks:
                if mark.first_value is not None:
                    marks_list.append(mark.first_value)
                if mark.second_value is not None:
                    marks_list.append(mark.second_value)
            
            data.append(
                {
                    'lesson_name': lesson.name,
                    'mark': 'Нет' if len(marks_list) == 0 else round(sum(marks_list) / len(marks_list))
                }
            )
                    

    return data