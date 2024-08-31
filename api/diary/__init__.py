from fastapi import APIRouter
from .create import create_diary_dp
from .info import diary_info_dp
from .quarter_info import quarter_info_dp
from .update import update_diary_dp
from .delete import delete_diary_dp
from .report import report_dp

diary_dp = APIRouter()

diary_dp.include_router(create_diary_dp, prefix='/create')
diary_dp.include_router(update_diary_dp, prefix='/update')
diary_dp.include_router(delete_diary_dp)
diary_dp.include_router(report_dp, prefix='/report')
diary_dp.include_router(diary_info_dp, prefix='/get-all')
diary_dp.include_router(quarter_info_dp, prefix='/get-quarter')