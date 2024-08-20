import json
from flask import Blueprint, request
from sqlalchemy import delete

from db.lesson import Lesson
from db.mark import Mark
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_marks_dp = Blueprint('mark_delete', __name__)


@delete_marks_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data: dict = request.get_json()
    user_id = tg_data['user']['id']


    diary = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary._id == data['diary_id']).first()
    lesson = session.query(Lesson).where(Lesson.attached_to_diary == diary._id).where(Lesson._id == data['lesson_id']).first()

    delete_query = delete(Mark).where(Mark.attached_to_lesson == lesson._id)

    if data.get('mark_ids') is not None:
        delete_query = delete_query.where(Mark._id.in_(tuple(data.get('mark_ids'))))

    session.execute(delete_query)
    session.commit()

    return ''