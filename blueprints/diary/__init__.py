__all__ = ['user_dp']

from flask import Blueprint
from .create import create_diary_dp
from .info import diary_info_dp
from .update import update_diary_dp
from .delete import delete_diary_dp

diary_dp = Blueprint('diary', __name__)

diary_dp.register_blueprint(create_diary_dp, url_prefix='/create')
diary_dp.register_blueprint(update_diary_dp, url_prefix='/update')
diary_dp.register_blueprint(delete_diary_dp, url_prefix='/delete')
diary_dp.register_blueprint(diary_info_dp, url_prefix='/get-all')