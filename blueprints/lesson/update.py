import json
from flask import Blueprint, request
from sqlalchemy import update
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lessons import Lesson


update_lesson_dp = Blueprint('lesson_update', __name__)


@update_lesson_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']


    upd = data.get('fields')

    diary = session.query(VirtualDiary).where(VirtualDiary._id == data['attached_to']).where(VirtualDiary.attached_to == user_id).first()

    session.execute(update(Lesson).where(Lesson._id == data['id']).where(Lesson.attached_to_diary == diary._id).values(**upd))
        
    session.commit()
    return ''