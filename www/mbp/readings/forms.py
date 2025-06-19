from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, DataRequired, ValidationError

class NewReadingForm(FlaskForm):
    systolic = IntegerField('Systolic', validators=[InputRequired(), NumberRange(min=50, max=160, message="This value must be between 50 to 160.")])
    diastolic = IntegerField('Diastolic', validators=[InputRequired(), NumberRange(min=50, max=160, message="This value must be between 50 to 160")])
    notes = TextAreaField('Notes', validators=[InputRequired(), Length(max=200)])

<<<<<<< HEAD
    submit = SubmitField('Reading')
=======
    submit = SubmitField('Reading')

>>>>>>> f4f24b8318672830d6dcc9f68606a325abbc60be
