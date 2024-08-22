__all__ = ['user_dp']

from flask import Blueprint
from .create import create_diary_dp
from .info import diary_info_dp
from .quarter_info import quarter_info_dp
from .update import update_diary_dp
from .delete import delete_diary_dp
from .report import create_report_dp, download_report_dp

diary_dp = Blueprint('diary', __name__)

diary_dp.register_blueprint(create_diary_dp, url_prefix='/create')
diary_dp.register_blueprint(update_diary_dp, url_prefix='/update')
diary_dp.register_blueprint(delete_diary_dp, url_prefix='/delete')
diary_dp.register_blueprint(create_report_dp, url_prefix='/report/create')
diary_dp.register_blueprint(download_report_dp, url_prefix='/report/download')
diary_dp.register_blueprint(diary_info_dp, url_prefix='/get-all')
diary_dp.register_blueprint(quarter_info_dp, url_prefix='/get-quarter')