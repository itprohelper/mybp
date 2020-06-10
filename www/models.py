from index import db
from forms import FlaskForm
from datetime import datetime
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import create_engine

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    join_date = db.Column(db.DateTime)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    reading = db.relationship('Readings', backref='patient', lazy='dynamic')

    def __repr__(self):
        # return '<User %r>' % self.username, self.email, self.picture
        return f"User('{self.username}', '{self.email}', '{self.picture}')"

class Readings(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    systolic = db.Column(db.Integer())
    diastolic = db.Column(db.Integer())
    notes = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f"Readings('{self.date}', '{self.systolic}', '{self.diastolic}', '{self.notes}')"

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
