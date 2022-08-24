from turtle import title
from flask import render_template, jsonify, redirect, url_for
import json
from mbp import app, db

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

@app.route('/about')
def about():
    return render_template('about.html', title='About')
