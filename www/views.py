from index import app
from index import db
from models import User, Readings, datetime
from forms import LoginForm, SignupForm, NewReading
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

            return '<h1>Invalid username or password</h1>'

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

    return render_template('signup.html', form=form)

@app.route('/dashboard')
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
    return render_template('dashboard.html', form=form)

# @app.route('/newreading', methods = ['GET','POST'])
# def newreading():
#     #form = NewReading()
#
#     #if form.validate_on_submit():
#         #Todo todaydate = datetime.now()
#         #new_reading = Readings(date=form.date.data, systolic=form.systolic.data, diastolic=form.diastolic.data, notes=form.notes.data)
#         # date = 'somedate'
#         # systolic = Systolic(systolic=form.systolic.data)
#         # diastolic = Diastolic(diastolic=form.diastolic.data)
#         # notes = Notes(notes=form.notes.data)
#
#
#     if request.method == 'POST':
#         tdate = datetime.now()
#         date = tdate;
#         #date = request.form['date']
#         systolic = request.form['systolic']
#         diastolic = request.form['diastolic']
#         notes = request.form['notes']
#
#
#         my_data = Readings(date,systolic, diastolic, notes)
#         # db.session.add(new_reading)
#         db.session.add(my_data)
#         db.session.commit()
#
#         flash("New reading created successfully")
#
#     return redirect(url_for('dashboard'))

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
