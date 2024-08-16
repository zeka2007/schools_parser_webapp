__all__ = ['Schoolsby_api', 'config']
import Schoolsby_api
import config
from db import db_url, database
from flask import Flask
from blueprints.api.main import api_dp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['BOT_TOKEN'] = config.bot_token
app.config['CORS_HEADERS'] = 'Content-Type'

database.init_app(app)

app.register_blueprint(api_dp, url_prefix='/api')

if __name__ == '__main__':
    app.run(
        debug=config.debug
    )
