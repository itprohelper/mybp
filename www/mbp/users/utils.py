import os
import secrets
from PIL import Image #Pillow library to resize image in Account page.
from flask import url_for, current_app
from flask_mail import Message
from mbp import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #saves filename in hex
    _, f_ext = os.path.splitext(form_picture.filename) #save filename with same extension: png or jpg
    picture_fn = random_hex + f_ext #combine random hex with filename - concatane both together
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    #resize image using the Pillow library
    output_size = (125, 125) #set to 125x125 pixels
    i = Image.open(form_picture) #create new image
    i.thumbnail(output_size) #resize image
    i.save(picture_path) #save new image thumnail

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender=os.getenv('APPROVED_SENDER'),
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email. No changes will be made to your account.
'''
    mail.send(msg)
