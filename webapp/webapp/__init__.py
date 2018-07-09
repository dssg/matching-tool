from flask import Flask
import os
from webapp.dbconfig import dburl
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.contrib.fixers import ProxyFix



SCHEMA_DIRECTORY = 'schemas/uploader/'

# Create app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['DEBUG'] = os.environ.get('DEBUG', True)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'salt')
app.config['SQLALCHEMY_DATABASE_URI'] = dburl
app.config["JSON_SORT_KEYS"] = False
app.config["SECURITY_RECOVERABLE"] = True
app.config["TESTING"] = True
app.config["LOGIN_DISABLED"] = True
app.config["MAIL_SERVER"] = os.environ.get('MAIL_SERVER', 'localhost')
app.config["MAIL_USE_TLS"] = os.environ.get('MAIL_USE_TLS', False)
app.config["MAIL_USE_SSL"] = os.environ.get('MAIL_USE_SSL', True)
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME', None)
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD', None)
app.config["MAIL_DEBUG"] = False
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get('MAIL_DEFAULT_SENDER', None)
app.config["SECURITY_EMAIL_SENDER"] = os.environ.get('MAIL_DEFAULT_SENDER', None)
app.config["MAIL_PORT"] = os.environ.get('MAIL_PORT', 465)


db = SQLAlchemy(app)
mail = Mail(app)


from webapp.tasks import match_finished
