from flask import Flask, render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from webapp.database import db_session
from webapp.models import User, Role, Upload, MergeLog
import yaml
from webapp.apis.upload import upload_api

# Create app
app = Flask(__name__)
with open('flask_config.yaml') as f:
    config = yaml.load(f)
    for key, val in config.items():
        app.config[key] = val

app.register_blueprint(upload_api)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def home(path):
    return render_template('index.html')

if __name__ == "__main__":
	app.run()
