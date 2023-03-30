from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from mbp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Database model definitions:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    readings = db.relationship('Reading', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800): #Expires in 30min. 1800seconds.
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) #use our secret key.
        return s.dumps({'user_id': self.id}).decode('utf-8') #Return token created with Serializer in utf-8

    #Method to verify token above
    @staticmethod #tell python we're using a static method. Not to expect 'self' parameter as an argument.
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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
