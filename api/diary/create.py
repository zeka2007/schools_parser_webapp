from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from db import get_session, student
from sqlalchemy.ext.asyncio import AsyncSession
from .. import validate
from db.virtual_diary import VirtualDiary
from db.diary import Diary


create_diary_dp = APIRouter()

class CreateDiaryExtend(BaseModel):
    type: str = None
    id: int

class CreateDiary(BaseModel):
    name: str
    extend: CreateDiaryExtend = None


async def is_main_diary(session: AsyncSession, user_id: int) -> bool:
    is_diary_main_result = await session.execute(select(func.count(Diary._id)).where(Diary.attached_to == user_id).where(Diary.is_main == True))
    is_diary_main = is_diary_main_result.scalar_one()

    is_v_diary_main_result = await session.execute(select(func.count(VirtualDiary._id)).where(VirtualDiary.attached_to == user_id).where(VirtualDiary.is_main == True))
    is_v_diary_main = is_v_diary_main_result.scalar_one()

    return not (is_diary_main or is_v_diary_main)


@create_diary_dp.post('/')
async def create_diary(data: CreateDiary, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    db_student_result = await session.execute(select(student.Student).where(student.Student.user_id == user_id))
    db_student = db_student_result.scalars().one_or_none()


    if db_student is None:
        session.add(
            student.Student(
                user_id=user_id,
            )
        )
    else: 
        db_diary_count_result = await session.execute(select(func.count(VirtualDiary._id)).where(VirtualDiary.attached_to == db_student.user_id).where(VirtualDiary.name == data.name))

        if db_diary_count_result.scalar() != 0:
            raise HTTPException(status_code=409)

    await session.commit()

    

    is_main = await is_main_diary(session, user_id)

    v_diary = VirtualDiary(
            name=data.name,
            attached_to=user_id,
            is_main=is_main
        )

    session.add(
        v_diary
    )

    await session.commit()
    await session.flush()
    await session.refresh(v_diary)

    return {'id': v_diary._id}
        