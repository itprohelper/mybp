from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '7930d939680d2fd3af6576162305e65f'

db = SQLAlchemy(app)

from mbp import views
