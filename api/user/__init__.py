from fastapi import APIRouter
from .login import login_api_dp
from .info import user_info_api_dp
from .delete import delete_student_dp

user_dp = APIRouter()

user_dp.include_router(login_api_dp, prefix='/login')
user_dp.include_router(user_info_api_dp, prefix='/get-data')
user_dp.include_router(delete_student_dp, prefix='/delete')