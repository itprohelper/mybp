import os
from flask import Flask, Markup
from flask import render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text



app = Flask(__name__)

app.config.from_pyfile('config.py')

# Configure MySQL connection.
db = SQLAlchemy(app)


from views import *



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
