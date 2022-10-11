from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, DataRequired, ValidationError

class NewReadingForm(FlaskForm):
    #date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()]) #difficult to enter day without from wtforms.fields.html5 import DateField
    systolic = IntegerField('Systolic', validators=[InputRequired(), NumberRange(min=50, max=160, message="This value must be between 50 to 160.")])
    diastolic = IntegerField('Diastolic', validators=[InputRequired(), NumberRange(min=50, max=160, message="This value must be between 50 to 160")])
    notes = TextAreaField('Notes', validators=[InputRequired(), Length(max=200)])
<<<<<<< HEAD
    submit = SubmitField('Reading')
=======
    submit = SubmitField('Reading')
>>>>>>> 239e7cc0063d2caea276dd99a61fd9a5abdf5c04
