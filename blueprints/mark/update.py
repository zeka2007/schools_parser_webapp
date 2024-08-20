from datetime import datetime
import json
from flask import Blueprint, abort, request
from sqlalchemy import update

from db.mark import Mark
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


update_mark_dp = Blueprint('mark_update', __name__)


@update_mark_dp.route('/', methods=['POST'])

@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()['data']
    user_id = tg_data['user']['id']

    diary = session.query(VirtualDiary).where(VirtualDiary._id == data['diary_id']).where(VirtualDiary.attached_to == user_id).first()

    lesson = session.query(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == data['attached_to_lesson']).first()

    data.pop('diary_id')
    data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")

    session.execute(update(Mark).where(Mark.attached_to_lesson == lesson._id).where(Mark._id == request.get_json()['id']).values(**data))

    session.commit()
   
    return ''