from mbp import app
from mbp import db
from mbp.models import User, Readings, Doctor, datetime
from mbp.forms import LoginForm, SignupForm, NewReading
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

        flash("Invalid username of password")


    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        #porque?
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists.')
            return redirect(url_for('signup'))

        db.session.add(new_user)
        db.session.commit()

        flash("New account created successfully")

    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NewReading()
    all_readings = Readings.query.all()
    return render_template(
        'dashboard.html', name=current_user.username, all_readings=all_readings, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/newreading', methods=['GET', 'POST'])
def newreading():
    form = NewReading()
    if  form.validate_on_submit():
        date = form.date.data
        systolic = form.systolic.data
        diastolic = form.diastolic.data
        notes = form.notes.data
        
        new_reading = Readings(date=date,systolic=systolic, diastolic=diastolic, notes=notes,user_id=current_user.id)
        db.session.add(new_reading)
        db.session.commit()

        flash("New reading created successfully")

        return redirect(url_for('dashboard'))
    return render_template('newreading.html', form=form)


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

@app.route('/deletereading/<id>', methods = ['GET', 'POST'])
def deletereading(id):
    d_data = Readings.query.get(id)
    db.session.delete(d_data)
    db.session.commit()
    flash("Readings deleted successfully")

    return redirect(url_for('dashboard'))


@app.route('/settings')
def settings():
    return render_template('settings.html', title= 'Account Settings')

@app.route('/reports')
def reports():
    return 'Reports here'

@app.route('/export')
def export():
    return 'Export here'

@app.route('/about')
def about():
  return 'Hola About MBP'