from datetime import datetime
from mbp import db


#Database model definitions:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    readings = db.relationship('Reading', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sys = db.Column(db.String(3), nullable=False)
    dia = db.Column(db.String(3), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Reading('{self.sys}', '{self.dia}', '{self.notes}, '{self.date_posted}'')"
