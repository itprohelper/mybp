from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy import create_engine
from index import db

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    join_date = db.Column(db.DateTime)
    picture = db.Column(db.String(250))
    reading = db.relationship('Readings', backref='user', lazy='dynamic')

    def __repr_(self):
        return '<User %r>' % self.username

class Readings(Base):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    systolic = db.Column(db.Integer())
    diastolic = db.Column(db.Integer())
    notes = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Doctor(Base):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


engine = create_engine('mysql://root:supersecure@db/mbp')


Base.metadata.create_all(engine)
