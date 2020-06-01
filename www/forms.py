from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, DateField, TextAreaField, DecimalField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, DataRequired
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Submit')
    remember = BooleanField('Remember me')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class NewReading(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()]) #difficult to enter day without from wtforms.fields.html5 import DateField
    systolic = IntegerField('Systolic', validators=[NumberRange(min=60, max=160, message="This value must be between 60 to 190.")])
    diastolic = IntegerField('Diastolic', validators=[InputRequired(), NumberRange(min=50, max=140, message="This value must be between 50 to 140")])
    notes = TextAreaField('Notes', validators=[InputRequired(), Length(max=120)])
    submit = SubmitField('Add Reading')
