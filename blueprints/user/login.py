from typing import List
from flask import Blueprint, request, abort
import json

from sqlalchemy import exists

from Schoolsby_api import Schools_by
from blueprints.diary.create import is_main_diary
from .. import validate
from db import database
from db.diary import Diary, get_schoolsby_student
from db.virtual_diary import VirtualDiary
from db import student


login_api_dp = Blueprint('login_api',
                    __name__)

@login_api_dp.route('/', methods = ['POST'])
@validate.validate
async def index(tg_data):
    login_data = request.get_json()
    session = database.session

    user: Schools_by.Student | None = await Schools_by.WebUser().login_user(login_data['login'], login_data['password'])
    
    if user is None:
        return abort(403)
    

    if not login_data['saveData']:
        user.login = None
        user.password = None

    user_id = tg_data['user']['id']


    db_diary = session.query(Diary).where(
            Diary.student_id == user.student_id
        ).where(
            Diary.attached_to == user_id
        ).one_or_none()

    db_student = session.query(student.Student).where(student.Student.user_id == user_id).one_or_none()


    if db_student is None:
        session.add(
            student.Student(
                user_id=user_id,
            )
        )

    is_main = is_main_diary(session, user_id)

    id = None

    if db_diary is not None:

        db_diary.login=user.login
        db_diary.password=user.password
        db_diary.csrf_token=user.csrf_token
        db_diary.session_id=user.session_id
        db_diary.student_id=user.student_id
        db_diary.site_prefix=user.site_prefix
        db_diary.is_main = is_main

        id = db_diary._id

        database.session.commit()

    else:
        diary = Diary(
                        attached_to=user_id,
                        login=user.login,
                        password=user.password,
                        csrf_token=user.csrf_token,
                        session_id=user.session_id,
                        student_id=user.student_id,
                        site_prefix=user.site_prefix,
                        is_main=is_main
                    )

        session.add(diary)

        database.session.commit()

        database.session.flush()
        database.session.refresh(diary)

        id = diary._id
    
    return json.dumps({'id':id})
