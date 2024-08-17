from flask import Blueprint
from .user import user_dp
from .diary import diary_dp

api_dp = Blueprint('api', __name__)

api_dp.register_blueprint(user_dp, url_prefix='/user')
api_dp.register_blueprint(diary_dp, url_prefix='/diary')
