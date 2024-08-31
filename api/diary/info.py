import json
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .consts import VIRTUAL_DIARY, SCHOOLS_BY_DIARY
from db import get_session
from .. import validate
from db.virtual_diary import VirtualDiary
from db.diary import Diary


diary_info_dp = APIRouter()


@diary_info_dp.get('/')
async def get_diaries_data(tg_data = Depends(validate.validate), session: AsyncSession = Depends(get_session)):
    user_id = tg_data['user']['id']

    diaries_result = await session.execute(select(Diary).where(Diary.attached_to == user_id))
    diaries = diaries_result.scalars().all()
    virtual_diaries_result = await session.execute(select(VirtualDiary).where(VirtualDiary.attached_to == user_id))
    virtual_diaries = virtual_diaries_result.scalars().all()

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
                'id': diary._id,
                'is_main': diary.is_main
            }
        )

    return data