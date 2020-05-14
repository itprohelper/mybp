from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, DateField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class NewReading(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    systolic = IntegerField('Systolic', validators=[InputRequired()])
    diastolic = IntegerField('Diastolic', validators=[InputRequired()])
    notes = TextAreaField('Notes', validators=[InputRequired(), Length(max=120)])
    submit = SubmitField('Submit')
