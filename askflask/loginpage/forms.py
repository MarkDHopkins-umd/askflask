from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError )
import pyotp

from ..models import User

def validate_password(form,field):
    special=0
    caps=0
    illegal=0
    arr=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    for i in field.data:
        if i == '@' or i== '$' or i== '&' or i== '#':
            special=special+1
        if i in arr:
            caps=caps+1
    if field.data[-1] == '\\' or field.data[-1] == '*' or field.data[-1] == '/':
        illegal=illegal+1
                 
    if special == 0 or caps==0:
        raise ValidationError('You must use at least 1 special character such as (@,$,&,or #) and at least 1 uppercase character.')
    if illegal > 0:
          raise ValidationError('You cannot include /, \, or a trailing * symbol.')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=32), validate_password])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):        
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')

    
class LoginForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    password=PasswordField('Password', validators=[InputRequired(), Length(min=8, max=32)])
    token= StringField('Token', validators=[InputRequired(), Length(min=6, max=6)])
    submit = SubmitField('Login')

    def validate_token(self, token):
        user = User.objects(username=self.username.data).first()
        if user is not None:
             tok_verified = pyotp.TOTP(user.otp_secret).verify(token.data)
             if not tok_verified:
                raise ValidationError("Invalid Token")

class UpdateUsernameForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField('Update Username')


