from flask import Blueprint, request
import json
from Schoolsby_api import Schools_by
from . import validate
from db import database, Student, get_schoolsby_student


user_api_dp = Blueprint('user_api', __name__)

@user_api_dp.route('/')
@validate.validate
async def get_user_data():
    data = validate.convert_to_dict(request.headers['Authorization'])
    user = database.get_or_404(Student, json.loads(data['user'])['id'])
    web_student: Schools_by.Student = get_schoolsby_student(user)

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
        ln = item.lesson.name
        marks_list = Schools_by.MarksManager.convert_marks_list([item])[0]

        if ln not in lessons_dict.keys():
            lessons_dict[ln] = []
        lessons_dict[ln].append(marks_list)

        flag = False
        for dindex, d in enumerate(lessons):
            if d['lesson_name'] == ln:
                lessons[dindex]['marks'].append(marks_list)
                flag = True
                break
        if not flag:
            lessons.append({
                    'lesson_name': ln,
                    'marks': [marks_list]
                })

    best_lesson = max(list(lessons_dict.items()), key=lambda x: sum(x[1]))[0]

    return_data = {
        'user': {
            'student_id': web_student.student_id,
            'quarter': quarter
        },
        'lessons': lessons,
        'average_mark': round(sum(converted_marks)/len(converted_marks), 2),
        'most_common': max(set(converted_marks), key=converted_marks.count),
        'marks_count': len(converted_marks),
        'best_lesson': {
            'lesson': best_lesson,
            'average_mark': round(sum(lessons_dict[best_lesson])/len(lessons_dict[best_lesson]), 2)
        }
        #TODO: add another fields
    }

    return json.dumps(return_data)
