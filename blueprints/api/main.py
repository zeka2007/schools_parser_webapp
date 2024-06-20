from flask import Blueprint, request
from .login_api import login_api_dp
from .user_api import user_api_dp

api_dp = Blueprint('api', __name__)

api_dp.register_blueprint(login_api_dp, url_prefix='/login')
api_dp.register_blueprint(user_api_dp, url_prefix='/get-user-data')