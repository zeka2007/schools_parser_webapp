from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from .. import validate
from db import get_session
from db.virtual_diary import VirtualDiary
from db.diary import Diary


update_diary_dp = APIRouter()


@update_diary_dp.post('/')
async def update_diary(data: dict, tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    diary = None

    print(data)

    if data['type'] == VIRTUAL_DIARY:
        diary_result = await session.execute(select(VirtualDiary).where(VirtualDiary._id == data['id']).where(VirtualDiary.attached_to == user_id))
        diary = diary_result.scalars().first()
    elif data['type'] == SCHOOLS_BY_DIARY:
        diary_result = await session.execute(select(Diary).where(Diary._id == data['id']).where(Diary.attached_to == user_id))
        diary = diary_result.scalars().first()

    if data.get('is_main') is not None:
        await session.execute(update(Diary).where(Diary.attached_to == user_id).where(Diary.is_main == True).values(is_main = False))
        await session.execute(update(VirtualDiary).where(VirtualDiary.attached_to == user_id).where(VirtualDiary.is_main == True).values(is_main = False))
        await session.execute(update(diary.__class__).where(diary.__class__._id == diary._id).values(is_main=data.get('is_main')))

    if data.get('other') is not None:
        await session.execute(update(diary.__class__).where(diary.__class__._id == diary._id).values(**data.get('other')))


    await session.commit()
    