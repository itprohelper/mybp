from index import app
from models import User
from forms import LoginForm, RegisterForm
from flask import render_template
from flask_bootstrap import Bootstrap

Bootstrap(app)

@app.route('/')
def home():
    firstmember = User.query.first()
    return '<h1>The first user is: ' + firstmember.name +'</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)

@app.route('/signup')
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
  return 'Hola About MBP'
