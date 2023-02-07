from flask import render_template, request, Blueprint
from mbp.models import Reading

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int) #Grab the page we want. In this case page one. Set type integer as the page number.
    reading = Reading.query.order_by(Reading.date_posted.desc()).paginate(page=page, per_page=6) #Show 5 readings per page. Can use http://localhost:8000/home?page=3 to navigate to pages.
    return render_template('index.html', reading=reading)


@main.route('/about')
def about():
    return render_template('about.html', title='About')