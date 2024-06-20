from flask import Blueprint, url_for, render_template, request

index_dp = Blueprint('index',
                        __name__,
                        template_folder='templates',
                        static_folder='static')


@index_dp.route('/')
def index():
    return render_template("i.html")
