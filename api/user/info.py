from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Schoolsby_api import Schools_by
from Schoolsby_api.Schools_by.MarksManager import Mark, SplitMark
from api.diary.consts import SCHOOLS_BY_DIARY_INT, VIRTUAL_DIARY, SCHOOLS_BY_DIARY, VIRTUAL_DIARY_INT
from db.lesson import Lesson
from db.virtual_diary import VirtualDiary
from .. import validate
from db import get_session
from db.diary import Diary, get_schoolsby_student
from db.mark import Mark as DBMark

user_info_api_dp = APIRouter()

@user_info_api_dp.get('/')
async def get_user_data(
    type: int = None,
    id: int = None,
    quarter: int = None,
    tg_data = Depends(validate.validate),
    session: AsyncSession = Depends(get_session)):

    d_type = type
    d_id = id
    quarter_arg = quarter

    user_id = tg_data['user']['id']

    v_diary = None
    user = None


    if (d_type is not None and d_id is not None):
        if d_type == SCHOOLS_BY_DIARY_INT:
            user_result = await session.execute(select(Diary).where(Diary.attached_to == user_id).where(Diary._id == int(d_id)))
            user = user_result.scalars().first()
        elif d_type == VIRTUAL_DIARY_INT:
            v_diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == int(d_id)))
            v_diary = v_diary_result.scalars().first()

    else:
        user_result = await session.scalars(select(Diary).where(Diary.attached_to == user_id).where(Diary.is_main == True))
        user = user_result.first()

    lessons = []
    lessons_dict = {}


    if user is None: 
        if v_diary is None:
            v_diary_result = await session.scalars(select(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary.is_main == True))
            v_diary = v_diary_result.first()

            if v_diary is None: 
                raise HTTPException(status_code=404)
            
        v_lessons_result = await session.scalars(select(Lesson).where(Lesson.attached_to_diary == v_diary._id))
        v_lessons = v_lessons_result.all()

        converted_marks = []

        for l in v_lessons:
            v_marks = []

            q = int(quarter_arg) if quarter_arg is not None else v_diary.quarter

            marks_result = await session.scalars(select(DBMark).where(DBMark.attached_to_lesson == l._id).where(DBMark.quarter == q))
            marks = marks_result.all()
            for v_mark in marks:
                marks_d = v_mark.__dict__
                marks_d.pop('_sa_instance_state')
                marks_d.pop('quarter')
                marks_d['date'] = v_mark.date.strftime('%Y-%m-%d')
                if v_mark.first_value is not None:
                    converted_marks.append(v_mark.first_value)
                    if v_mark.second_value:
                        converted_marks.append(v_mark.second_value)

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
                'diary_id': user._id,
                'is_login_date_saved': user.login is not None and user.password is not None
            },
            'lessons': lessons
        }

    if len(converted_marks) > 0: 
        return_data.update(
            {
                'average_mark': round(sum(converted_marks)/len(converted_marks), 2),
                'most_common': max(set(converted_marks), key=converted_marks.count),
                'marks_count': len(converted_marks)
            }
        )

    return return_data
