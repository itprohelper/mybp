import os

class Config:
    SECRET_KEY = '7930d939680d2fd3af6576162305e65f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

 #DEGUG = True
 #SQLALCHEMY_DATABASE_URI = 'mysql://root:supersecure@db/mbp'
 #SECRET_KEY = 'supersecure1'
