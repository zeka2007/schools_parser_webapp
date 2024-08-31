import os
from typing import List
import uuid
from fastapi.responses import FileResponse
import pandas
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark, SplitMark
from db.lesson import Lesson
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from db import get_session
from .. import validate
from db.virtual_diary import VirtualDiary
from db.diary import Diary, get_schoolsby_student
from db.mark import Mark as DBMark


report_dp = APIRouter()

SAVE_PATH = './data/reports/'

class CreateReport(BaseModel):
    type: str
    id: int
    quarters: List[int]


@report_dp.post('/create')
async def create_report(
        data: CreateReport,
        tg_data = Depends(validate.validate),
        session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    data.quarters.sort()

    sheets = [{}, {}, {}, {}]

    if data.type == VIRTUAL_DIARY:
        diary_id_result = await session.execute(select(VirtualDiary._id).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == data.id))
        diary_id = diary_id_result.scalar()
        lessons_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == diary_id))
        lessons = lessons_result.scalars().all()
        for lesson in lessons:
            for quarter in data.quarters:
                db_marks_result = await session.execute(select(DBMark).where(DBMark.attached_to_lesson == lesson._id).where(DBMark.quarter == quarter))
                db_marks = db_marks_result.scalars().all()
                mark_data = {}
                for m in db_marks:
                    converted_date = m.date.strftime('%d.%m.%Y')
                    if m.first_value is None:
                        mark_data[converted_date] = m.display_value
                    else:
                        if m.second_value is not None:
                            mark_data[converted_date] = f'{m.first_value}/{m.second_value}'
                        else:
                            mark_data[converted_date] = str(m.first_value)
                sheets[quarter - 1][lesson.name] = mark_data
    


    elif data.type == SCHOOLS_BY_DIARY:
        diary_result = await session.execute(select(Diary).where(Diary.attached_to == user_id).where(Diary._id == data.id))
        diary = diary_result.scalars().first()
        web_student: Schools_by.Student = get_schoolsby_student(diary)

        for quarter in data.quarters:
            marks = await Schools_by.MarksManager.get_all_marks(web_student, quarter)
            mark_data = {}

            for item in marks:
                item: Mark | SplitMark
                ln = item.lesson.name

                converted_date = m.date.strftime('%d.%m.%Y')

                if item.__class__ == Mark:
                    mark_text = str(item.value)

                if item.__class__ == SplitMark:
                    mark_text = f'{item.first_mark}/{item.second_mark}'

                sheets[quarter - 1][ln][converted_date] = mark_text
                

    file_id = str(uuid.uuid4())

    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    writer = pandas.ExcelWriter(f'{SAVE_PATH}{file_id}.xlsx', engine='xlsxwriter')

    i = 1
    for s in sheets:
        if s != {}:
            pandas.DataFrame(s).to_excel(writer, sheet_name=f'Четверть {i}')
        i += 1

    writer._save()
            
    return {'file_id': file_id}


@report_dp.get('/download/{filename}')
async def download_report(filename: str):
    return FileResponse(path=os.path.join(SAVE_PATH, f'{filename}.xlsx'), filename='export.xlsx')