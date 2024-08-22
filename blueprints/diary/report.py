import json
import os
import uuid
import pandas
from flask import Blueprint, request, send_file

from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark, SplitMark
from db.lesson import Lesson
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from db import student
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary, get_schoolsby_student
from db.mark import Mark as DBMark


create_report_dp = Blueprint('diary_create_report', __name__)
download_report_dp = Blueprint('diary_download_report', __name__)

SAVE_PATH = './data/reports/'


@create_report_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    user_id = tg_data['user']['id']
    data = request.get_json()

    data['quarters'].sort()

    sheets = [{}, {}, {}, {}]

    if data['type'] == VIRTUAL_DIARY:
        diary_id: int | None = session.query(VirtualDiary._id).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == data['id']).scalar()
        lessons = session.query(Lesson).where(Lesson.attached_to_diary == diary_id).all()
        for lesson in lessons:
            for quarter in data['quarters']:
                db_marks = session.query(DBMark).where(DBMark.attached_to_lesson == lesson._id).where(DBMark.quarter == quarter).all()
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
    


    elif data['type'] == SCHOOLS_BY_DIARY:
        diary = session.query(Diary).where(Diary.attached_to == user_id).where(Diary._id == data['id']).first()
        web_student: Schools_by.Student = get_schoolsby_student(diary)

        for quarter in data['quarters']:
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
            print(pandas.DataFrame(s).head())# to_excel(writer, sheet_name=f'Четверть {i}')
        i += 1

    writer._save()
            
    return json.dumps({'file_id': file_id})

@download_report_dp.route('/<string:filename>')
async def index_3(filename):
    return send_file(os.path.join(SAVE_PATH, f'{filename}.xlsx'), download_name='export.xlsx', as_attachment=True)