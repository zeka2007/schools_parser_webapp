__all__ = ['user_dp']

from flask import Blueprint
from .create import create_mark_dp
from .update import update_mark_dp
from .delete import delete_marks_dp
# from .delete_marks import delete_lesson_marks_dp
from .info import mark_info_dp

mark_dp = Blueprint('mark', __name__)

mark_dp.register_blueprint(create_mark_dp, url_prefix='/create')
mark_dp.register_blueprint(update_mark_dp, url_prefix='/update')
mark_dp.register_blueprint(delete_marks_dp, url_prefix='/delete')
# lesson_dp.register_blueprint(delete_lesson_marks_dp, url_prefix='/delete-marks')
mark_dp.register_blueprint(mark_info_dp, url_prefix='/get-all')