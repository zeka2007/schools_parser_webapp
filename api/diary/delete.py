from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db.lesson import Lesson
from db.mark import Mark
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from .. import validate
from db.virtual_diary import VirtualDiary
from db.diary import Diary


delete_diary_dp = APIRouter()

class DeleteDiary(BaseModel):
    type: str
    id: int

class DeleteLoginData(BaseModel):
    diary_id: int


@delete_diary_dp.post('/delete')
async def delete_diary(data: DeleteDiary, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    if data.type == VIRTUAL_DIARY:
        await session.execute(delete(VirtualDiary).where(VirtualDiary._id == data.id).where(VirtualDiary.attached_to == user_id))
        lessons_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == data.id))
        lessons = lessons_result.scalars().all()
        for lesson in lessons:
            await session.execute(delete(Mark).where(Mark.attached_to_lesson == lesson._id))
        await session.execute(delete(Lesson).where(Lesson.attached_to_diary == data.id))
    elif data.type == SCHOOLS_BY_DIARY:
        await session.execute(delete(Diary).where(Diary._id == data.id).where(Diary.attached_to == user_id))

    await session.commit()


@delete_diary_dp.post('/delete-all')
async def delete_all_diaries(tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']
    
    v_diaries_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id))
    v_diaries = v_diaries_result.scalars().all()

    for v_diary in v_diaries:
        lessons_result = await session.execute(select(Lesson).where(Lesson.attached_to_diary == v_diary._id))
        lessons = lessons_result.scalars().all()
        for lesson in lessons:
            await session.execute(delete(Mark).where(Mark.attached_to_lesson == lesson._id))
        await session.execute(delete(Lesson).where(Lesson.attached_to_diary == v_diary._id))

    await session.execute(delete(VirtualDiary).where(VirtualDiary.attached_to == user_id))
    await session.execute(delete(Diary).where(Diary.attached_to == user_id))

    await session.commit()



@delete_diary_dp.post('/delete-login-data')
async def delete_login_data(data: DeleteLoginData, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    await session.execute(update(Diary).where(Diary.attached_to == user_id).where(Diary._id == data.diary_id).values(
        login=None,
        password=None
    ))

    await session.commit()
    