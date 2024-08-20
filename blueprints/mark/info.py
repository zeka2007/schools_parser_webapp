import json
from flask import Blueprint, request

from db.mark import Mark
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


mark_info_dp = Blueprint('mark_info', __name__)


@mark_info_dp.route('/')
@validate.validate
async def index(tg_data):
    session = database.session
    user_id = tg_data['user']['id']
    diary_id = request.args.get('diary_id')
    lesson_id = request.args.get('lesson_id')
    quarter = request.args.get('quarter')

    diary = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == diary_id).first()

    lesson = session.query(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == lesson_id).first()
    marks = session.query(Mark).where(Mark.attached_to_lesson == lesson._id).where(Mark.quarter == quarter).order_by(Mark.date).all()

    data = []

    for m in marks:
        mark_dict = m.__dict__
        mark_dict.pop('_sa_instance_state')
        mark_dict['date'] = m.date.strftime('%Y-%m-%d')
        mark_dict.pop('quarter')
        data.append(mark_dict)    

    return json.dumps(data), {'Content-Type': 'application/json; charset=utf-8'}