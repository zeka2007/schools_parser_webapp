import json
from flask import Blueprint, abort, request
from datetime import datetime
from sqlalchemy import update
from db import student
from db.mark import Mark
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


create_mark_dp = Blueprint('mark_create', __name__)


@create_mark_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    diary = session.query(VirtualDiary).where(VirtualDiary._id == data['diary_id']).where(VirtualDiary.attached_to == user_id).first()

    lesson = session.query(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == data['attached_to_lesson']).first()

    if lesson is None: return abort(404)

    data.pop('diary_id')
    data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")

    mark = Mark(**data)
    session.add(mark)

    session.commit()
    session.flush()
    session.refresh(mark)

    return json.dumps({'id': mark._id}), {'Content-Type': 'application/json; charset=utf-8'}