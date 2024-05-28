__all__ = ['Schoolsby_api', 'config']
import Schoolsby_api
import config
from db import db_url, database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blueprints.index.index import index_dp
from blueprints.login.login import login_dp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

database.init_app(app)


app.register_blueprint(index_dp)
app.register_blueprint(login_dp, url_prefix='/login')


if __name__ == '__main__':
    app.run(
        debug=config.debug
    )
