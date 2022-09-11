from flask import render_template, jsonify, redirect, flash, url_for
import json
from mbp import app
from mbp.models import User, Reading
from mbp.forms import RegistrationForm, LoginForm

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success') #Display flash confirmation message.
        return redirect(url_for('home'))    #When the form is a success redirect to home page.
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home')) #If the above matches return to Home page showing the flash message.
        else: #When not a success login do this.
            flash('Login no good. Please check username and password', 'danger') #It will return to login page displaying this message.
    return render_template('login.html', title='Login', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')
