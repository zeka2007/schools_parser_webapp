__all__ = ['user_dp']

from flask import Blueprint
from .create import create_lesson_dp
from .update import update_lesson_dp
from .delete import delete_lesson_dp
from .delete_marks import delete_lesson_marks_dp
from .info import lesson_info_dp

lesson_dp = Blueprint('lesson', __name__)

lesson_dp.register_blueprint(create_lesson_dp, url_prefix='/create')
lesson_dp.register_blueprint(update_lesson_dp, url_prefix='/update')
lesson_dp.register_blueprint(delete_lesson_dp, url_prefix='/delete')
lesson_dp.register_blueprint(delete_lesson_marks_dp, url_prefix='/delete-marks')
lesson_dp.register_blueprint(lesson_info_dp, url_prefix='/get-all')