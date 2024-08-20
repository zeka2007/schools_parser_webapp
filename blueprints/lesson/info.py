import json
from flask import Blueprint, request

from db.mark import Mark
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lesson import Lesson


lesson_info_dp = Blueprint('lesson_info', __name__)


@lesson_info_dp.route('/')
@validate.validate
async def index(tg_data):
    session = database.session
    user_id = tg_data['user']['id']
    diary_id = request.args.get('diary_id')

    diary = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == diary_id).first()

    lessons = session.query(Lesson).where(Lesson.attached_to_diary == diary._id).all()

    data = []


    for l in lessons:
        marks_data = session.query(Mark).where(Mark.attached_to_lesson == l._id).all()
        marks = [[], [], [], []]

        for m in marks_data:
            mark_dict = m.__dict__
            mark_dict.pop('_sa_instance_state')
            mark_dict['date'] = m.date.strftime('%m-%d-%Y')
            marks[m.quarter - 1].append(mark_dict)
            mark_dict.pop('quarter')


        data.append({
                "id": l._id, 
                "name": l.name, 
                "attached_to_diary": l.attached_to_diary, 
                "marks": marks
            } )    
    
    return json.dumps(data), {'Content-Type': 'application/json; charset=utf-8'}