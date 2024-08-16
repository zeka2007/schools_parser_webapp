from flask import Blueprint, request
from db import student
from . import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


diary_api_dp = Blueprint('diary_api', __name__)

@diary_api_dp.route('/get-all')
@validate.validate
async def get_user_data(tg_data):
    session = database.session
    user_id = tg_data['user']['id']

    diares = session.query(Diary).where(Diary.attached_to == user_id)
    virtual_diares = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id)

    return 'afd'



@diary_api_dp.route('/create', methods=['POST'])
@validate.validate
async def get_user_data(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    db_student = session.query(student.Student).where(student.Student.user_id == user_id).one_or_none()


    if db_student is None:
        session.add(
            student.Student(
                user_id=user_id,
            )
        )

    session.add(
        VirtualDiary(
            name=data['name'],
            attached_to=user_id
        )
    )

    session.commit()

    return '{}'