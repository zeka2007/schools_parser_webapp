from datetime import datetime
from flask import Blueprint, request
import json

from sqlalchemy import select
from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark, SplitMark
from . import validate
from db import database
from db.student import Student
from db.diary import Diary, get_schoolsby_student

user_api_dp = Blueprint('user_api', __name__)

@user_api_dp.route('/get-data')
@validate.validate
async def get_user_data(tg_data):

    user_id = tg_data['user']['id']
    session = database.session

    users = session.scalars(select(Diary).where(Diary.attached_to == user_id)).all()

    web_student: Schools_by.Student = get_schoolsby_student(users[0])

    quarter_arg = request.args.get('quarter')
    if (quarter_arg is None):
        quarter = await Schools_by.QuarterManager.get_current_quarter(web_student)
    else:
        quarter = int(quarter_arg)
    marks = await Schools_by.MarksManager.get_all_marks(web_student, quarter)
    converted_marks = Schools_by.MarksManager.convert_marks_list(marks)

    lessons = []
    lessons_dict = {}

    for item in marks:
        item: Mark | SplitMark
        ln = item.lesson.name

        marks_obj = {}

        if item.__class__ == Mark:
            marks_obj = {
                        'first_value': item.value,
                        'date': item.date.strftime("%Y-%m-%d")
                    }
            

        if item.__class__ == SplitMark:
            marks_obj = {
                    'first_value': item.first_mark,
                    'second_value': item.second_mark,
                    'date': item.date.strftime("%Y-%m-%d")
                }
            
        

        if ln not in lessons_dict.keys():
            lessons_dict[ln] = []
        lessons_dict[ln].append(marks_obj)

        flag = False
        for dindex, d in enumerate(lessons):
            if d['lesson_name'] == ln:
                lessons[dindex]['marks'].append(marks_obj)
                flag = True
                break
        if not flag:
            lessons.append({
                    'lesson_name': ln,
                    'marks': [marks_obj]
                })
            
    #TODO:
            
    best_lesson = 'Матем.' # max(list(lessons_dict.items()), key=lambda x: sum([it['first_value'] for it in x[1]]))[0]

    return_data = {
        'user': {
            'student_id': web_student.student_id,
            'quarter': quarter
        },
        'lessons': lessons
    }

    if len(converted_marks) > 0: 
        return_data.update(
            {
                'average_mark': round(sum(converted_marks)/len(converted_marks), 2),
                'most_common': max(set(converted_marks), key=converted_marks.count),
                'marks_count': len(converted_marks),
                'best_lesson': {
                    'lesson': best_lesson,
                    'average_mark': 4.54 #round(sum(lessons_dict[best_lesson])/len(lessons_dict[best_lesson]), 2)
                }
            }
        )

    return json.dumps(return_data), {'Content-Type': 'application/json; charset=utf-8'}
