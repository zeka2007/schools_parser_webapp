from flask import Blueprint, request, abort
import json

from Schoolsby_api import Schools_by


login_api_dp = Blueprint('login_api',
                    __name__)

@login_api_dp.route('/', methods = ['GET', 'POST'])
# @cross_origin()
async def index():
    data = request.get_json()
    user: Schools_by.Student = await Schools_by.WebUser().login_user(data['login'], data['password'])

    if user is None:
        return abort(403)
    
    if not data['save_login_data']:
        user.login = None
        user.password = None

    user.cookies = None
    
    return json.dumps(user.__dict__)
