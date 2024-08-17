__all__ = ['user_dp']

from flask import Blueprint
from .login import login_api_dp
from .info import user_info_api_dp

user_dp = Blueprint('user', __name__)

user_dp.register_blueprint(login_api_dp, url_prefix='/login')
user_dp.register_blueprint(user_info_api_dp, url_prefix='/get-data')