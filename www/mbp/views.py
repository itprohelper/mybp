import os
import secrets
from PIL import Image #Pillow library to resize image in Account page.
from crypt import methods
from flask import render_template, jsonify, redirect, flash, url_for, request, abort
import json
from mbp import app, db, bcrypt, mail
from mbp.models import User, Reading
from mbp.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                       NewReadingForm, RequestResetForm, ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

#readings = [
#    {
#        'user': 'Francisco Ulloa',
#        'sys': '122',
#        'dia': '77',
#        'notes': 'Oyendo perico ripiao',
#        'date': 'Aug 4, 2022 at 4:07PM'
#    },
#    {
#        'user': 'Pakar Kuruturuntun',
#        'sys': '140',
#        'dia': '90',
#        'notes': 'Oyendo Tika Tike Tuka',
#        'date': 'Aug 5, 2022 at 6:23PM'
#    }
#]


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int) #Grab the page we want. In this case page one. Set type integer as the page number.
    reading = Reading.query.order_by(Reading.date_posted.desc()).paginate(page=page, per_page=5) #Show 5 readings per page. Can use http://localhost:8000/home?page=3 to navigate to pages.
    return render_template('index.html', reading=reading)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home')) #check if the current user if logged in and redirect to home page.
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) #Add user to database
        db.session.commit() #Commit changes to database
        flash('Your account has been created!', 'success') #Display flash confirmation message.
        return redirect(url_for('login')) #When the form is a success redirect to login page.
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) #check if the current user if logged in and redirect to home page.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #query database for user entered in form.
        if user and bcrypt.check_password_hash(user.password, form.password.data): #check if user exists and check hashed password and what the user entered in the form.
            login_user(user, remember=form.remember.data) #login the user if it exist and password is correct also pass in the remember me checkbox.
            next_page = request.args.get('next') #no estoy claro porque todavia.
            return redirect(next_page) if next_page else redirect(url_for('home')) #send user back to home page if all good.
        else:
            flash('Login no good. Please check email and password', 'danger') #then user will be redirected to login page.
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #saves filename in hex
    _, f_ext = os.path.splitext(form_picture.filename) #save filename with same extension: png or jpg
    picture_fn = random_hex + f_ext #combine random hex with filename - concatane both together
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #resize image using the Pillow library
    output_size = (125, 125) #set to 125x125 pixels
    i = Image.open(form_picture) #create new image
    i.thumbnail(output_size) #resize image
    i.save(picture_path) #save new image thumnail

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET': #if a GET populate user's current data in the form.
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/reading/new/', methods=['GET', 'POST'])
@login_required
def new_reading():
    form = NewReadingForm()
    if form.validate_on_submit():
        reading = Reading(sys=form.systolic.data, dia=form.diastolic.data, notes=form.notes.data, user=current_user)
        db.session.add(reading)
        db.session.commit()
        flash('Your reading has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_reading.html', title='New Reading',
                            form=form, legend='New Reading')

@app.route('/reading/<int:reading_id>/')
def reading(reading_id):
    reading = Reading.query.get_or_404(reading_id)
    return render_template('reading.html', title='User Readings', reading=reading)

@app.route('/reading/<int:reading_id>/update', methods=['GET', 'POST'])
@login_required
def update_reading(reading_id):
    reading = Reading.query.get_or_404(reading_id)
    if reading.user != current_user:
        abort(403)
    form = NewReadingForm()
    if form.validate_on_submit():
        reading.sys = form.systolic.data
        reading.dia = form.diastolic.data
        reading.notes = form.notes.data
        db.session.commit()
        flash('Your readings have been updated!', 'success')
        return redirect(url_for('reading', reading_id=reading.id))
    elif request.method == 'GET':
        form.systolic.data = reading.sys
        form.diastolic.data = reading.dia
        form.notes.data = reading.notes
    return render_template('new_reading.html', title='Update Reading',
                            form=form, legend='Update Reading') #using the same template for new reading. Using legend to display different titles.

@app.route('/reading/<int:reading_id>/delete', methods=['POST'])
@login_required
def delete_reading(reading_id):
    reading = Reading.query.get_or_404(reading_id)
    if reading.user != current_user:
        abort(403)
    db.session.delete(reading)
    db.session.commit()
    flash('Your readings have been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_readings(username):
    page = request.args.get('page', 1, type=int) #Grab the page we want. In this case page one. Set type integer as the page number.
    user = User.query.filter_by(username=username).first_or_404()
    reading = Reading.query.filter_by(user=user)\
        .order_by(Reading.date_posted.desc())\
        .paginate(page=page, per_page=5) #Show 5 readings per page. Can use http://localhost:8000/home?page=3 to navigate to pages.
    return render_template('user_readings.html', reading=reading, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Requet',
                    sender='mbp@itprohelper.com',
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email. No changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent for resetting your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST']) #pass in the token in the URL
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token) #pass in the token
    if user is None: #if condition is met then the token was valid and we got the user. We can display the update form for the user.
        flash('That is an invalid or expired token,' 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit() #Commit changes to database
        flash('Your password has been updated! You can now login.', 'success') #Display flash confirmation message.
        return redirect(url_for('login')) #When the form is a success redirect to login page.

    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')
