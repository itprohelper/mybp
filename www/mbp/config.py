import os

class Config:
    #SECRET_KEY = '7930d939680d2fd3af6576162305e65f'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

 #DEGUG = True
 #SQLALCHEMY_DATABASE_URI = 'mysql://root:supersecure@db/mbp'
 #SECRET_KEY = 'supersecure1'