from index import db
from forms import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    picture = db.Column(db.String(250))

class LoginForm(FlaskForm):
    username = StringField('username')
    email = StringField('email')
    password = PasswordField('password')
    remember = BooleanField('remember me')

#class LoginForm(FlaskForm):
#    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
#    remember = BooleanField('remember me')

#class SignupForm(FlaskForm):
#    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
class SignupForm(FlaskForm):
    username = StringField('username')
    email = StringField('email')
    password = StringField('password')
