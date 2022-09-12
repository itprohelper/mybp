from flask import render_template, jsonify, redirect, flash, url_for, request
import json
from mbp import app, db, bcrypt
from mbp.models import User, Reading
from mbp.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

readings = [
    {
        'user': 'Francisco Ulloa',
        'sys': '122',
        'dia': '77',
        'notes': 'Oyendo perico ripiao',
        'date': 'Aug 4, 2022 at 4:07PM'
    },
    {
        'user': 'Pakar Kuruturuntun',
        'sys': '140',
        'dia': '90',
        'notes': 'Oyendo Tika Tike Tuka',
        'date': 'Aug 5, 2022 at 6:23PM'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', readings=readings)

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

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route('/about')
def about():
    return render_template('about.html', title='About')
