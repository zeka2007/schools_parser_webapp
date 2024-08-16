from flask import Blueprint
from .login import login_api_dp
from .user import user_api_dp
from .diary import diary_api_dp

api_dp = Blueprint('api', __name__)

api_dp.register_blueprint(login_api_dp, url_prefix='/login')
api_dp.register_blueprint(user_api_dp, url_prefix='/user')
api_dp.register_blueprint(diary_api_dp, url_prefix='/diary')
