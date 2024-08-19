import json
from flask import Blueprint, request
from sqlalchemy import update
from db import student
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lessons import Lesson


create_lesson_dp = Blueprint('lesson_create', __name__)


@create_lesson_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    diary = session.query(VirtualDiary).where(VirtualDiary._id == data['diary_id']).where(VirtualDiary.attached_to == user_id).first()

    lesson: Lesson = Lesson(
        name=data['name'],
        attached_to_diary=diary._id,
        marks=[[], [], [], []]
    )

    session.add(lesson)

    session.commit()
    session.flush()
    session.refresh(lesson)

    return json.dumps({'id': lesson._id}), {'Content-Type': 'application/json; charset=utf-8'}