import json
from flask import Blueprint, request
from sqlalchemy import delete

from db.lesson import Lesson
from db.mark import Mark
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_diary_dp = Blueprint('diary_delete', __name__)


@delete_diary_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    diary = None

    if data['type'] == VIRTUAL_DIARY:
        session.execute(delete(VirtualDiary).where(VirtualDiary._id == data['id']).where(VirtualDiary.attached_to == user_id))
        lessons = session.query(Lesson).where(Lesson.attached_to_diary == data['id']).all()
        for lesson in lessons:
            session.execute(delete(Mark).where(Mark.attached_to_lesson == lesson._id))
        session.execute(delete(Lesson).where(Lesson.attached_to_diary == data['id']))
    elif data['type'] == SCHOOLS_BY_DIARY:
        session.execute(delete(Diary).where(Diary._id == data['id']).where(Diary.attached_to == user_id))

    session.commit()

    return ''