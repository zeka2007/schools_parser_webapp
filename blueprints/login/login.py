from flask import Blueprint, render_template, url_for, request, abort
import json

login_dp = Blueprint(
    'login', __name__,
    template_folder='templates',
    static_folder='static'
)

@login_dp.route('/')
async def index():
    return render_template("login.html")