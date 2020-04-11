import os
from flask import Flask, Markup
from flask import render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config.from_pyfile('config.py')

# Configure MySQL connection.
db = SQLAlchemy(app)


from views import *
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
