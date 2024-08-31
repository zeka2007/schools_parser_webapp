from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from Schoolsby_api import Schools_by
from api.diary.create import is_main_diary
from .. import validate
from db import get_session
from db.diary import Diary
from db import student


login_api_dp = APIRouter()

class LoginData(BaseModel):
    login: str
    password: str
    saveData: bool


@login_api_dp.post('/')
async def login_user_diary(login_data: LoginData, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):

    user: Schools_by.Student | None = await Schools_by.WebUser().login_user(login_data.login, login_data.password)
    
    if user is None:
        raise HTTPException(status_code=403)

    
    if not login_data.saveData:
        user.login = None
        user.password = None

    user_id = tg_data['user']['id']


    db_diary_result = await session.execute(select(Diary).where(
            Diary.student_id == user.student_id
        ).where(
            Diary.attached_to == user_id
        ))
    
    db_diary = db_diary_result.scalars().one_or_none()

    db_student_result = await session.execute(select(student.Student).where(student.Student.user_id == user_id))
    db_student = db_student_result.scalars().one_or_none()


    if db_student is None:
        session.add(
            student.Student(
                user_id=user_id,
            )
        )

    is_main = await is_main_diary(session, user_id)

    id = None

    if db_diary is not None:

        id = db_diary._id

        await session.execute(update(Diary).where(Diary._id == id).values(
            login=user.login,
            password=user.password,
            csrf_token=user.csrf_token,
            session_id=user.session_id,
            student_id=user.student_id,
            site_prefix=user.site_prefix,
            is_main=is_main
        ))

        await session.commit()

    else:
        diary = Diary(
                        attached_to=user_id,
                        login=user.login,
                        password=user.password,
                        csrf_token=user.csrf_token,
                        session_id=user.session_id,
                        student_id=user.student_id,
                        site_prefix=user.site_prefix,
                        is_main=is_main
                    )

        session.add(diary)

        await session.commit()

        await session.flush()
        await session.refresh(diary)

        id = diary._id
    
    return {'id':id}
