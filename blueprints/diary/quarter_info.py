import json
from typing import List
from flask import Blueprint, request
from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark
from db.lesson import Lesson
from .consts import SCHOOLS_BY_DIARY_INT, VIRTUAL_DIARY_INT
from db import student
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary, get_schoolsby_student
from db.mark import Mark as DBMark


quarter_info_dp = Blueprint('quarter_info', __name__)


@quarter_info_dp.route('/')
@validate.validate
async def index(tg_data):
    session = database.session
    user_id = tg_data['user']['id']
    params = request.args
    data = []

    if params['type'] == SCHOOLS_BY_DIARY_INT:
        diary = session.query(Diary).where(Diary.attached_to == user_id).where(Diary._id == params['diary_id']).first()
        web_user = get_schoolsby_student(diary)
        marks: List[Mark] = await Schools_by.MarksManager.get_quarters_marks(web_user, int(params['quarter']))
        for mark in marks:
            data.append(
                {
                    'lesson_name': mark.lesson.full_name,
                    'mark': 'Нет' if mark.value is None else mark.value
                }
            )
    elif params['type'] == VIRTUAL_DIARY_INT:
        diary_id: int | None = session.query(VirtualDiary._id).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == params['diary_id']).scalar()
        lessons = session.query(Lesson).where(Lesson.attached_to_diary == diary_id).all()
        for lesson in lessons:
            db_marks = session.query(DBMark).where(DBMark.attached_to_lesson == lesson._id).where(DBMark.quarter == params['quarter']).all()
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
                    

    return json.dumps(data), {'Content-Type': 'application/json; charset=utf-8'}