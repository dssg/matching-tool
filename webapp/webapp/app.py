from flask import render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from webapp import app
from webapp.database import db_session
from webapp.models import User, Role
from webapp.apis.upload import upload_api
from webapp.apis.chart import chart_api
import os

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)
app.register_blueprint(upload_api)
app.register_blueprint(chart_api)


@app.route('/test')
def test():
    return "success!"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def home(path):
    return render_template('index.html')

