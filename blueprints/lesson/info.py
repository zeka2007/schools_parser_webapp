import json
from flask import Blueprint, request
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.lessons import Lesson


lesson_info_dp = Blueprint('lesson_info', __name__)


@lesson_info_dp.route('/')
@validate.validate
async def index(tg_data):
    session = database.session
    user_id = tg_data['user']['id']
    diary_id = request.args.get('diary_id')

    diary = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == diary_id).first()

    lessons = session.query(Lesson).where(Lesson.attached_to_diary == diary._id).all()

    data = [{"id": l._id, "name": l.name, "attached_to_diary": l.attached_to_diary} for l in lessons]        
    
    return json.dumps(data), {'Content-Type': 'application/json; charset=utf-8'}