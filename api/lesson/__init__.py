from fastapi import APIRouter
from .create import create_lesson_dp
from .update import update_lesson_dp
from .delete import delete_lesson_dp
from .info import lesson_info_dp

lesson_dp = APIRouter()

lesson_dp.include_router(create_lesson_dp, prefix='/create')
lesson_dp.include_router(update_lesson_dp, prefix='/update')
lesson_dp.include_router(delete_lesson_dp, prefix='/delete')
lesson_dp.include_router(lesson_info_dp, prefix='/get-all')