from flask import Flask
import os
from webapp.dbconfig import dburl
from flask_sqlalchemy import SQLAlchemy



SCHEMA_DIRECTORY = 'schemas/uploader/'

# Create app
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DEBUG'] = os.environ['DEBUG']
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SECURITY_PASSWORD_SALT']
app.config['SQLALCHEMY_DATABASE_URI'] = dburl
app.config["JSON_SORT_KEYS"] = False


db = SQLAlchemy(app)
