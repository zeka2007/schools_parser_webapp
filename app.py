__all__ = ['Schoolsby_api', 'config']
from datetime import datetime
import os
import Schoolsby_api
import config
from db import db_url, database
from flask import Flask
from blueprints.main import api_dp
from flask_cors import CORS
from flask_apscheduler import APScheduler
from blueprints.diary.report import SAVE_PATH

app = Flask(__name__)

CORS(app)
scheduler = APScheduler()

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['BOT_TOKEN'] = config.bot_token
app.config['CORS_HEADERS'] = 'Content-Type'

database.init_app(app)
scheduler.init_app(app)

@scheduler.task('interval', id='autoremove_reports', hours=1)
def autoremove_reports():
    current_date = datetime.now()
    for file in os.listdir(SAVE_PATH):
        m_time = os.path.getmtime(SAVE_PATH + file)
        dt_m = datetime.fromtimestamp(m_time)
        diff = current_date - dt_m
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        if (hours >= 1): 
            os.remove(SAVE_PATH + file)

scheduler.start()

app.register_blueprint(api_dp, url_prefix='/api')

if __name__ == '__main__':
    app.run(
        debug=config.debug
    )
