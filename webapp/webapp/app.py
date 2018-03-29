from flask import render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from webapp import app
from webapp.database import db_session
from webapp.models import User, Role
from webapp.apis.upload import upload_api
from webapp.apis.chart import chart_api
from webapp.apis.jobs import jobs_api
import os

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)
app.register_blueprint(upload_api)
app.register_blueprint(chart_api)
app.register_blueprint(jobs_api)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def home(path):
    return render_template('index.html')

