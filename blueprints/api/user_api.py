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
        return ' '.join(Schools_by.MarksManager.convert_marks_list(marks))


        # user: Schools_by.Student = await Schools_by.WebUser().login_user(data['login'], data['password'])

    return abort(400)
