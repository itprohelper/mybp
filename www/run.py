from mbp import app

from mbp import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy import create_engine, asc, desc
 
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(90))
    join_date = db.Column(db.DateTime)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    readings = db.relationship('Readings', backref='creator', lazy=True)

    def __repr__(self):
        # return '<User %r>' % self.username, self.email, self.picture
        return f"User('{self.username}', '{self.email}', '{self.picture}')"

class Readings(Base):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    systolic = db.Column(db.Integer())
    diastolic = db.Column(db.Integer())
    notes = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Readings('{self.date_posted}', '{self.systolic}', '{self.diastolic}', '{self.notes}')" 

class Doctor(Base):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(150), unique=False)
    doctor_email = db.Column(db.String(50), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


engine = create_engine('mysql://root:supersecure@db/mbp')
 

Base.metadata.create_all(engine)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
