from flask import Blueprint, render_template, url_for, request, abort
from Schoolsby_api import Schools_by

login_dp = Blueprint(
    'login', __name__,
    template_folder='templates',
    static_folder='static'
    )


@login_dp.route('/', methods = ['GET', 'POST'])
async def index():
    if request.method == 'POST':
        data = request.get_json()
        user: Schools_by.Student = await Schools_by.WebUser().login_user(data['login'], data['password'])
        if user is None:
            return abort(403)
        return str(user.student_id)
    return render_template("login.html")