
from flask import render_template, jsonify, request
import json
from mbp import app, db
#from www.forms import CreateUser, UpdateUser

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/users')
def otro_hello_world():
    return 'Otro HOla!'
