import json
from flask import Blueprint, request
from sqlalchemy import update
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from db import student, lessons
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


update_diary_dp = Blueprint('diary_update', __name__)


@update_diary_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    diary = None

    if data['type'] == VIRTUAL_DIARY:
        diary = session.query(VirtualDiary).where(VirtualDiary._id == data['id']).where(VirtualDiary.attached_to == user_id).first()
    elif data['type'] == SCHOOLS_BY_DIARY:
        diary = session.query(Diary).where(Diary._id == data['id']).where(Diary.attached_to == user_id).first()

    if data.get('is_main') is not None:
        session.execute(update(Diary).where(Diary.attached_to == user_id).where(Diary.is_main == True).values(is_main = False))
        session.execute(update(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary.is_main == True).values(is_main = False))

        diary.is_main = data.get('is_main')

    if data.get('other') is not None:
        for key in data['other'].keys():
            diary.__dict__[key] = data['other'][key]

            print(diary.name)


            session.commit()
    

    return ''