from mbp import app
from mbp import db
from mbp.models import User, Readings, Doctor, datetime, desc, asc
from mbp.forms import LoginForm, SignupForm, NewReading, UpdateAccountForm, EditReading
from flask import render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import session as login_session

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
    if current_user.is_authenticated:  #redirect logged in users to dashboard
        return redirect(url_for('dashboard'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("New account created successfully")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NewReading()
    now = datetime.utcnow()
    current_user.systolic = form.systolic.data #porque esta linea?

    user_readings = db.session.query(Readings).filter_by(user_id=current_user.id).all()

    last_readings = db.session.query(Readings).filter_by(user_id=current_user.id).order_by(Readings.date_posted.desc()).limit(3).all()

    return render_template(
        'dashboard.html', now=now,name=current_user.username, systolic=current_user.systolic,
          user_id=current_user.id, user_readings=user_readings, last_readings=last_readings,form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/newreading', methods=['GET', 'POST'])
def newreading():

    form = NewReading()
    if  form.validate_on_submit():
        now = datetime.utcnow()
        #current_time = datetime.datetime.now()
        current_user.systolic = form.systolic.data
        current_user.diastolic = form.diastolic.data
        current_user.notes = form.notes.data

        new_reading = Readings(systolic=current_user.systolic, diastolic=current_user.diastolic, notes=current_user.notes,user_id=current_user.id)
        db.session.add(new_reading)
        db.session.commit()

        flash("New reading created successfully")

        return redirect(url_for('dashboard'))
    return render_template('newreading.html', form=form)


@app.route('/editreading/<id>', methods = ['GET', 'POST'])
@login_required
def editreading(id):
    e_reading = Readings.query.get_or_404(id)
    if e_reading.creator != current_user:
        abort(403)
    form = EditReading()
    if form.validate_on_submit():
        e_reading.systolic = form.systolic.data
        e_reading.diastolic = form.diastolic.data
        e_reading.notes = form.notes.data
        db.session.commit()
        flash('Your readings have been updated!')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.systolic.data = e_reading.systolic
        form.diastolic.data = e_reading.diastolic
        form.notes.data = e_reading.notes
    return render_template('editreading.html', form=form, title= 'Edit Readings and Notes')


@app.route('/deletereading/<id>', methods = ['GET', 'POST'])
def deletereading(id):
    d_data = Readings.query.get(id)
    db.session.delete(d_data)
    db.session.commit()
    flash("Readings deleted successfully")

    return redirect(url_for('dashboard'))


@app.route('/settings', methods=['GET', 'POST']) #hacer un query para ver los doctores del usuario?
@login_required
def settings():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.doctorName = form.doctorName.data
        current_user.doctorEmail = form.doctorEmail.data

        new_doctor = Doctor(doctorName=current_user.doctorName,doctorEmail=current_user.doctorEmail,user_id=current_user.id)
        db.session.add(new_doctor)
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.doctorName.data = current_user.doctorName


    picture = url_for('static', filename='profile_pics/' + current_user.picture)
    return render_template('settings.html', title= 'Account Settings', picture=picture, form=form)

@app.route('/reports')
def reports():
    return render_template('reports.html', title= 'Reports')

#@app.route('/export')
#def export():
#    return 'Export here'

@app.route('/about')
def about():
  return 'Hola About MBP'
