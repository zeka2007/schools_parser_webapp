from fastapi import APIRouter
from .user import user_dp
from .diary import diary_dp
from .lesson import lesson_dp
from .mark import mark_dp

api_dp = APIRouter(prefix='/api')

api_dp.include_router(user_dp, prefix='/user')
api_dp.include_router(diary_dp, prefix='/diary')
api_dp.include_router(lesson_dp, prefix='/lesson')
api_dp.include_router(mark_dp, prefix='/mark')
