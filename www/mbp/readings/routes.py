from flask import Blueprint
from flask import (render_template, url_for, flash,
                  redirect, request, abort)
from flask_login import login_user, current_user, logout_user, login_required
from mbp import db
from mbp.models import Reading
from mbp.readings.forms import NewReadingForm

readings = Blueprint('readings', __name__)

from flask import (render_template, jsonify, redirect, flash,
                    url_for, request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from mbp import db
from mbp.models import Post
from mbp.readings.forms import PostForm

readings = Blueprint('reading', __name__)
>>>>>>> 239e7cc0063d2caea276dd99a61fd9a5abdf5c04

@readings.route('/reading/new/', methods=['GET', 'POST'])
@login_required
def new_reading():
    form = NewReadingForm()
    if form.validate_on_submit():
        reading = Reading(sys=form.systolic.data, dia=form.diastolic.data, notes=form.notes.data, user=current_user)
        db.session.add(reading)
        db.session.commit()
        flash('Your reading has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_reading.html', title='New Reading',
                            form=form, legend='New Reading')

@readings.route('/reading/<int:reading_id>/')
def reading(reading_id):
    reading = Reading.query.get_or_404(reading_id)
    return render_template('reading.html', title='User Readings', reading=reading)

@readings.route('/reading/<int:reading_id>/update', methods=['GET', 'POST'])
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

        return redirect(url_for('reading.reading', reading_id=reading.id))

        return redirect(url_for('readings.reading', reading_id=reading.id))

    elif request.method == 'GET':
        form.systolic.data = reading.sys
        form.diastolic.data = reading.dia
        form.notes.data = reading.notes
    return render_template('new_reading.html', title='Update Reading',
                            form=form, legend='Update Reading') #using the same template for new reading. Using legend to display different titles.

@readings.route('/reading/<int:reading_id>/delete', methods=['POST'])
@login_required
def delete_reading(reading_id):
    reading = Reading.query.get_or_404(reading_id)
    if reading.user != current_user:
        abort(403)
    db.session.delete(reading)
    db.session.commit()
    flash('Your readings have been deleted!', 'success')

    return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))
