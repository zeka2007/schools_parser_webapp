from flask import Flask
from blueprints.index.index import index_dp
from blueprints.login.login import login_dp

app = Flask(__name__)
app.register_blueprint(index_dp)
app.register_blueprint(login_dp, url_prefix='/login')

if __name__ == '__main__':
    app.run(
        debug=True
    )
