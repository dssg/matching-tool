from flask import Flask, render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from webapp.database import db_session
from webapp.models import User, Role
# import yaml
from webapp.apis.upload import upload_api
from webapp.apis.chart import chart_api
import os

# Create app
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DEBUG'] = os.environ['DEBUG']
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SECURITY_PASSWORD_SALT']


app.register_blueprint(upload_api)
app.register_blueprint(chart_api)
# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)


@app.route('/test')
def test():
    return "success!"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def home(path):
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
