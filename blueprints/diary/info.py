import json
from flask import Blueprint, request
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from db import student
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


diary_info_dp = Blueprint('diary_info', __name__)


@diary_info_dp.route('/')
@validate.validate
async def get_user_data(tg_data):
    session = database.session
    user_id = tg_data['user']['id']

    diaries = session.query(Diary).where(Diary.attached_to == user_id).all()
    virtual_diaries = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).all()

    data = []

    diaries.extend(virtual_diaries)
    
    for diary in diaries:
        diary: Diary | VirtualDiary
        diary_type = ''
        name = ''
        if diary.__class__ == VirtualDiary:
           diary_type = VIRTUAL_DIARY
           name = diary.name
        elif diary.__class__ == Diary:
            diary_type = SCHOOLS_BY_DIARY
            name = str(diary.student_id)

        data.append(
            {
                'type': diary_type,
                'name': name,
                'id': diary._id
            }
        )

    return json.dumps(data), {'Content-Type': 'application/json; charset=utf-8'}