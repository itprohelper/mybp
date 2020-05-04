from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
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

class Doctor(Base):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(50), unique=True)

class Readings(Base):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    systolic = db.Column(db.Integer())
    diastolic = db.Column(db.Integer())
    notes = db.Column(db.String(250))

    @validates('systolic')
    def validate_systolic(self, key, value):
        assert value >= 0
        assert value <= 999
        return value



engine = create_engine('mysql://root:supersecure@db/mbp')


Base.metadata.create_all(engine)
