from flask import Blueprint, render_template, url_for, request

login_dp = Blueprint(
    'login', __name__,
    template_folder='templates',
    static_folder='static'
    )


@login_dp.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return request.get_json()['login'] + ' maybe ok'
    return render_template("login.html")