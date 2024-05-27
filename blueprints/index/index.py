from flask import Blueprint, url_for

index_dp = Blueprint('index', __name__, template_folder='templates', static_folder='static')


@index_dp.route('/')
def index():
    return 'Web app'
