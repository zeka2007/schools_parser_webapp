import json
from flask import Blueprint, request
from db import student
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


create_diary_dp = Blueprint('diary_create', __name__)


def is_main_diary(session, user_id: int) -> bool:
    is_diary_main = session.query(Diary).where(Diary.attached_to == user_id).where(Diary.is_main == True).count()
    is_v_diary_main = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary.is_main == True).count()

    print(is_diary_main, is_v_diary_main)

    return not (is_diary_main or is_v_diary_main)


@create_diary_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    data = request.get_json()
    user_id = tg_data['user']['id']

    db_student = session.query(student.Student).where(student.Student.user_id == user_id).one_or_none()


    if db_student is None:
        session.add(
            student.Student(
                user_id=user_id,
            )
        )

    session.commit()

    is_main = is_main_diary(session, user_id)

    v_diary = VirtualDiary(
            name=data['name'],
            attached_to=user_id,
            is_main=is_main
        )

    session.add(
        v_diary
    )

    session.commit()
    session.flush()
    session.refresh(v_diary)

    return json.dumps(
            {
                'id': v_diary._id
            }
        ) 