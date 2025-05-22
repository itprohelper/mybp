from flask import Blueprint
from flask import (render_template, url_for, flash,
                  redirect, request, abort)

from flask_login import login_user, current_user, logout_user, login_required
from mbp import db, bcrypt
from mbp.models import User, Reading
from mbp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            RequestResetForm, ResetPasswordForm)
from mbp.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# need to add this route to menu to be displayed ONLY to the current user logged in.
@users.route('/dashboard')
@login_required
def dashboard():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
   # page = request.args.get('page', 1, type=int) #Grab the page we want. In this case page one. Set type integer as the page number.
#    page = request.args.get('page', 1, type=int)
    #user = User.query.filter_by(username=username).first_or_404()
    lreading = Reading.query.order_by(Reading.id.desc()).first()
        
    #reading = Reading.query.filter_by(user=user)\
    #.order_by(Reading.date_posted.desc())\
    #.paginate(page=page, per_page=3) #displays last three readings in order. newest first.
    #if user != current_user:
    #    abort(403)
    #reading = Reading.query.order_by(Reading.date_posted.desc()).filter_by(user_id=current_user.id).all().paginate(page=page, per_page=5)
    #reading = Reading.query.order_by(Reading.date_posted.desc()).paginate(page=page, per_page=6) #Show 5 readings per page. Can use http://localhost:8000/home?page=3 to navigate to pages.
    return render_template('dashboard.html', title='Dashboard', image_file=image_file, lreading=lreading) #reading=reading, user=user)

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        #current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')

        return redirect(url_for('users.account'))

    elif request.method == 'GET': #if a GET populate user's current data in the form.
        form.username.data = current_user.username
        #form.username.data = current_user.email
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/user/<string:username>')
#@users.route('/user/<string:email>')
@login_required
def user_readings(username):
#def user_readings(email):
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    page = request.args.get('page', 1, type=int) #Grab the page we want. In this case page one. Set type integer as the page number.
    
    user = User.query.filter_by(username=username).first_or_404()
    #user = User.query.filter_by(email=email).first_or_404()
    lreading = Reading.query.filter_by(user=user).order_by(Reading.id.desc()).first()
    reading = Reading.query.filter_by(user=user)\
        .order_by(Reading.date_posted.desc())\
        .paginate(page=page, per_page=5) #Show 5 readings per page. Can use http://localhost:8000/home?page=3 to navigate to pages.
    return render_template('user_readings.html', title='User Dashboard', reading=reading, user=user, username=username, image_file=image_file, lreading=lreading)
    #return render_template('user_readings.html', title='User Dashboard', reading=reading, user=user, image_file=image_file, lreading=lreading)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) #check if the current user if logged in and redirect to home page.     
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) #Add user to database
        db.session.commit() #Commit changes to database
        print("User committed", user) #Debug only
        flash('Your account has been created!', 'success') #Display flash confirmation message.
        return redirect(url_for('users.login')) #When the form is a success redirect to login page.
    else:
        print(form.errors) #debugging line
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_readings', username=current_user.username)) #check if the current user is logged in and redirect to home page.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #query database for user entered in form.
        print(f"DEBUG: user from db = {user}")
        if user and bcrypt.check_password_hash(user.password, form.password.data): #check if user exists and check hashed password and what the user entered in the form.
            login_user(user, remember=form.remember.data) #login the user if it exist and password is correct also pass in the remember me checkbox.
            next_page = request.args.get('next') #para el target page por ejemplo si entras /account page sin estar login.

            return redirect(next_page) if next_page else redirect(url_for('users.user_readings', username=current_user.username)) #send user back to home page if all good.
            
        else:
            flash('Login no good. Please check email and password', 'danger') #then user will be redirected to login page.
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('main.home'))

@users.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent for resetting your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset-password/<token>', methods=['GET', 'POST']) #pass in the token in the URL
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token) #pass in the token
    if user is None: #if condition is met then the token was valid and we got the user. We can display the update form for the user.
        flash('That is an invalid or expired token,' 'warning')
        return redirect(url_for('utils.reset_request')) 
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit() #Commit changes to database
        flash('Your password has been updated! You can now login.', 'success') #Display flash confirmation message.

        return redirect(url_for('users.login')) #When the form is a success redirect to login page.
        
    return render_template('reset_token.html', title='Reset Password', form=form)
