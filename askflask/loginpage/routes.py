from flask import render_template, request, redirect, url_for, flash, Response, Blueprint, session
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import requests
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError )
# stdlib

# local
from datetime import datetime

# local
from .. import app, bcrypt, client, mail
from .forms import (RegistrationForm, LoginForm, UpdateUsernameForm)
from ..models import User, Question, load_user, Answers
from ..utils import current_time




loginpage= Blueprint('loginpage', __name__)
""" ************ View functions ************ """

@loginpage.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        requests.Session()
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        finalProjectUser = User(username=form.username.data, 
                    email=form.email.data, password=hashed)
        session['new_username'] = finalProjectUser  
        print('OTP secret:', finalProjectUser.otp_secret)
      
        finalProjectUser.save()
      
        flash('Please login')
        return redirect(url_for('loginpage.tfa'))
        
    return render_template('register.html', form=form)



@loginpage.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage.index'))
    form = LoginForm()  


    if form.validate_on_submit():

        user = User.objects(username=form.username.data).first()
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):  
            
            login_user(user)        
           
            return redirect(url_for('homepage.index'))
        else:
             flash('Wrong username or password.')
    return render_template('login.html', form=form)

 

@loginpage.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.index'))

@loginpage.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    
    form = UpdateUsernameForm()
    
    if form.validate_on_submit():
        if len(User.objects(username=form.username.data)) == 0:  
            current_user.modify(username=form.username.data)
            current_user.save()
           
            msg = Message("You changed your username!",
            recipients=User.objects(username=current_user.username).first().email.split())
            username= current_user.username
            msg.body = "You changed your username to "+username
            mail.send(msg)
            return redirect(url_for('loginpage.account'))           
        else:
            flash('This username is already taken!')                   
    return render_template('account.html', form=form, user=current_user)

@loginpage.route('/user/<username>')
def user_detail(username):
    user=load_user(username)
    if user is not None:
       
        return render_template('user_detail.html', user=username, questions= Question.objects(commenter=user.id), total=len(Question.objects(commenter=user.id)))
    return render_template('user_detail.html')

@loginpage.route("/tfa")
def tfa():
    if 'new_username' not in session:
        return redirect(url_for('homepage.index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return render_template('tfa.html'), headers

@loginpage.route("/qr_code")
def qr_code():
    if 'new_username' not in session:
        return redirect(url_for('homepage.index'))
   
    user = User.objects(username=session['new_username'].get("username")).first()
    session.pop('new_username')
    print('OTP secret:', user.otp_secret)
    uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name='AskFlask-2FA')
    img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return stream.getvalue(), headers

