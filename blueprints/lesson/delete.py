import json
from flask import Blueprint, request
from sqlalchemy import delete

from db.lesson import Lesson
from db.mark import Mark
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_lesson_dp = Blueprint('lesson_delete', __name__)


@delete_lesson_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    diary = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == data['diary_id']).first()

    session.execute(delete(Lesson).where(Lesson._id == data['id']).where(Lesson.attached_to_diary == diary._id))
    session.execute(delete(Mark).where(Mark.attached_to_lesson == data['id']))
    
    session.commit()

    return ''