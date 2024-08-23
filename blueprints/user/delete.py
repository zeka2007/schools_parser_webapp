import json
from flask import Blueprint
from sqlalchemy import delete

from db.lesson import Lesson
from db.mark import Mark
from db.student import Student
from .. import validate
from db import database
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_student_dp = Blueprint('student_delete', __name__)


@delete_student_dp.route('/', methods=['POST'])
@validate.validate
async def index(tg_data):
    session = database.session
    user_id = tg_data['user']['id']

    v_diaries = session.query(VirtualDiary).where(VirtualDiary.attached_to == user_id).all()

    for v_diary in v_diaries:
        lessons = session.query(Lesson).where(Lesson.attached_to_diary == v_diary._id).all()
        for lesson in lessons:
            session.execute(delete(Mark).where(Mark.attached_to_lesson == lesson._id))
        session.execute(delete(Lesson).where(Lesson.attached_to_diary == v_diary._id))

    session.execute(delete(VirtualDiary).where(VirtualDiary.attached_to == user_id))
    session.execute(delete(Diary).where(Diary.attached_to == user_id))
    session.execute(delete(Student).where(Student.user_id == user_id))

    session.commit()

    return ''