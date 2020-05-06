from index import app
from index import db
from models import User, Readings
from forms import LoginForm, SignupForm
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

            # if user.password == form.password.data:


        return '<h1>Invalid username or password</h1>'

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    #if form.validate_on_submit():
    #    return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
#         return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    all_readings = Readings.query.all()
    return render_template(
        'dashboard.html', name=current_user.username, all_readings=all_readings)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/newreading', methods = ['POST'])
def newreading():
    if request.method == 'POST':
        date = 'Todays date'
        # date = request.form['date']
        systolic = request.form['systolic']
        diastolic = request.form['diastolic']
        notes = request.form['notes']

        my_data = Readings(date, systolic, diastolic, notes)
        db.session.add(my_data)
        db.session.commit()

        flash("New reading created successfully")

        return redirect(url_for('dashboard'))

@app.route('/editreading', methods = ['GET', 'POST'])
def editreading():

    if request.method == 'POST':
        e_data = Readings.query.get(request.form.get('id'))

        e_data.systolic = request.form['systolic']
        e_data.diastolic = request.form['diastolic']
        e_data.notes = request.form['notes']

        db.session.commit()
        flash("Readings updated successfully")

        return redirect(url_for('dashboard'))

@app.route('/deletereading')
def deletereading():
    return 'Delete readings'

@app.route('/profile')
def profile():
    return 'Profile here'

@app.route('/settings')
def settings():
    return 'Settings here'

@app.route('/reports')
def reports():
    return 'Reports here'

@app.route('/export')
def export():
    return 'Export here'

@app.route('/about')
def about():
  return 'Hola About MBP'
