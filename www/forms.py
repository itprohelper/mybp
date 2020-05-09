from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class NewReading(FlaskForm):
    date = DateTimeField('date')
    systolic = IntegerField('systolic', validators=[InputRequired()])
    diastolic = IntegerField('diastolic', validators=[InputRequired()])
    notes = StringField('notes', validators=[InputRequired(), Length(max=180)])
