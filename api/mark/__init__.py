from fastapi import APIRouter
from .create import create_mark_dp
from .update import update_mark_dp
from .delete import delete_marks_dp
from .info import mark_info_dp

mark_dp = APIRouter()

mark_dp.include_router(create_mark_dp, prefix='/create')
mark_dp.include_router(update_mark_dp, prefix='/update')
mark_dp.include_router(delete_marks_dp, prefix='/delete')
mark_dp.include_router(mark_info_dp, prefix='/get-all')