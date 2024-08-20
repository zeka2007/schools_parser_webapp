from datetime import datetime
from flask import Blueprint, abort, request
import json

from sqlalchemy import select
from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark, SplitMark
from blueprints.diary.consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from db.lesson import Lesson
from db.virtual_diary import VirtualDiary
from .. import validate
from db import database
from db.student import Student
from db.diary import Diary, get_schoolsby_student
from db.mark import Mark as DBMark

user_info_api_dp = Blueprint('user_info', __name__)

@user_info_api_dp.route('/')
@validate.validate
async def index(tg_data):

    d_type = request.args.get('type')
    d_id = request.args.get('id')

    user_id = tg_data['user']['id']
    session = database.session

    v_diary = None
    user = None

    if (d_type and d_id):
        if d_type == '0':
            user = session.scalars(select(Diary).where(Diary.attached_to == user_id).where(Diary._id == int(d_id))).first()
        elif d_type == '1':
            v_diary = session.scalars(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == int(d_id))).first()

    else:
        user = session.scalars(select(Diary).where(Diary.attached_to == user_id).where(Diary.is_main == True)).first()

    lessons = []
    lessons_dict = {}

    
    if user is None: 
        if v_diary is None:
            v_diary = session.scalars(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary.is_main == True)).first()

            if v_diary is None: 
                return abort(404)
            
        v_lessons = session.scalars(select(Lesson).where(Lesson.attached_to_diary == v_diary._id)).all()

        for l in v_lessons:
            v_marks = []

            quarter_arg = request.args.get('quarter')

            q = int(quarter_arg) if quarter_arg is not None else v_diary.quarter

            marks = session.scalars(select(DBMark).where(DBMark.attached_to_lesson == l._id).where(DBMark.quarter == q)).all()
            for v_mark in marks:
                marks_d = v_mark.__dict__
                marks_d.pop('_sa_instance_state')
                marks_d.pop('quarter')
                marks_d['date'] = v_mark.date.strftime('%Y-%m-%d')
                v_marks.append(marks_d)

            if len(v_marks) > 0:
                lessons.append({
                            'lesson_name': l.name,
                            'marks': v_marks
                        })
        
        return_data = {
            'user': {
                'type': VIRTUAL_DIARY,
                'description': v_diary.name,
                'quarter': v_diary.quarter,
                'main_now': v_diary.is_main,
                'diary_id': v_diary._id
            },
            'lessons': lessons
        }


    else:
        web_student: Schools_by.Student = get_schoolsby_student(user)

        quarter_arg = request.args.get('quarter')
        if (quarter_arg is None):
            quarter = await Schools_by.QuarterManager.get_current_quarter(web_student)
        else:
            quarter = int(quarter_arg)
        marks = await Schools_by.MarksManager.get_all_marks(web_student, quarter)
        converted_marks = Schools_by.MarksManager.convert_marks_list(marks)

    
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

        return_data = {
            'user': {
                'type': SCHOOLS_BY_DIARY,
                'description': web_student.student_id,
                'quarter': quarter,
                'main_now': user.is_main,
                'diary_id': user._id
            },
            'lessons': lessons
        }

        if len(converted_marks) > 0: 
            best_lesson = max(list(lessons_dict.items()), key=lambda x: sum([it['first_value'] for it in x[1]]))[0]
            return_data.update(
                {
                    'average_mark': round(sum(converted_marks)/len(converted_marks), 2),
                    'most_common': max(set(converted_marks), key=converted_marks.count),
                    'marks_count': len(converted_marks),
                    'best_lesson': {
                        'lesson': best_lesson,
                        'average_mark': round(sum(lessons_dict[best_lesson])/len(lessons_dict[best_lesson]), 2)
                    }
                }
            )

    return json.dumps(return_data), {'Content-Type': 'application/json; charset=utf-8'}
