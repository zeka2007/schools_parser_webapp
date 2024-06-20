from flask import Blueprint, request, abort, current_app
import json
from Schoolsby_api import Schools_by
from . import validate
from db import database, Student, get_schoolsby_student


user_api_dp = Blueprint('user_api', __name__)

@user_api_dp.route('/')
async def get_user_data():
    data = request.args.to_dict()
    if validate.validate_init_data(data, current_app.config['BOT_TOKEN']):
        user = database.get_or_404(Student, json.loads(data['user'])['id'])
        web_student: Schools_by.Student = get_schoolsby_student(user)
        quarter = await Schools_by.QuarterManager.get_current_quarter(web_student)
        marks = await Schools_by.MarksManager.get_all_marks(web_student, quarter)
        converted_marks = Schools_by.MarksManager.convert_marks_list(marks)

        lessons = {}

        for item in marks:
            ln = item.lesson.name
            if ln not in lessons.keys():
                lessons[ln] = []
            lessons[ln].append(Schools_by.MarksManager.convert_marks_list([item])[0])

        best_lesson = max(list(lessons.items()), key=lambda x: sum(x[1]))[0]

        return_data = {
            'average_mark': round(sum(converted_marks)/len(converted_marks), 2),
            'most_common': max(set(converted_marks), key=converted_marks.count),
            'marks_count': len(converted_marks),
            'best_lesson': {
                'lesson': best_lesson,
                'average_mark': round(sum(lessons[best_lesson])/len(lessons[best_lesson]), 2)
            }
            #TODO: add another fields
        }

        return json.dumps(return_data)


        # user: Schools_by.Student = await Schools_by.WebUser().login_user(data['login'], data['password'])

    return abort(400)
