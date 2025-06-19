import os
from flask import Flask
from dotenv import load_dotenv
from mbp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
<<<<<<< HEAD
from flask_moment import Moment

load_dotenv()
=======
from mbp.config import Config
from flask_moment import Moment
>>>>>>> f4f24b8318672830d6dcc9f68606a325abbc60be

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info' #decorate the login message alert.
mail = Mail()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(Config)
<<<<<<< HEAD
    print("Using DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("DB file path:", os.path.abspath(os.path.join(app.instance_path, 'site.db')))
    
=======
>>>>>>> f4f24b8318672830d6dcc9f68606a325abbc60be
    moment.init_app(app)    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    
    from mbp.users.routes import users
    from mbp.readings.routes import readings
    from mbp.main.routes import main
    from mbp.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(readings)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app