import os
from flask import Flask, Markup
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, asc
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text



app = Flask(__name__)
moment = Moment(app)

app.config.from_pyfile('config.py')

# Configure MySQL connection.
db = SQLAlchemy(app)

from mbp import views
