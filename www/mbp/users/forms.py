from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, DataRequired, ValidationError
from flask_login import current_user #to validate user and email updates in UpdateAccountForm
from mbp.models import User #despues tengo que import Reading, Doctor y etc aqui



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    #username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Submit')
    remember = BooleanField('Remember me')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user: #Validates if user exist and show the below error
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: #Validates if email exist and show the below error
            raise ValidationError('That email is taken. Please choose a different one')

class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: #Validates if user exist and show the below error
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: #Validates if email exist and show the below error
                raise ValidationError('That email is taken. Please choose a different one')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:  #Validates if email exist and show the below error
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

#-------------------Older forms. Maybe will use later-----------------#
#class NewDoctor(FlaskForm):
#    doctor_name = StringField('Doctor Name', validators=[Length(min=0, max=15)]) #Need to validate opcional y que no haga un entry al DB if blank
#    doctor_email = StringField('Doctor Email', validators=[Length(max=50)]) #Need to validate opcional y que no haga un entry al DB if blank
#    submit = SubmitField('Add Doctor')

#class EditReading(FlaskForm):
#    systolic = IntegerField('Systolic', validators=[InputRequired(),NumberRange(min=60, max=160, message="This value must be between 60 to 160.")])
#    diastolic = IntegerField('Diastolic', validators=[InputRequired(), NumberRange(min=50, max=140, message="This value must be between 50 to 140")])
#    notes = TextAreaField('Notes', validators=[InputRequired(), Length(max=120)])
#    submit = SubmitField('Edit Reading')
