# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime
from flask_talisman import Talisman
from flask_mail import Mail
csp={
   'default-src': '\'self\'',
    'script-src': ['https://code.jquery.com/jquery-3.4.1.slim.min.js','https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js', 
    'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'],
    'style-src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
}

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/finalProject"

app.config['MONGODB_HOST'] = 'mongodb://heroku_rwvrz8xh:38reaudqd77rasbafg4qd1k5fd@ds149491.mlab.com:49491/heroku_rwvrz8xh?retryWrites=false'
#app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/project'
app.config['SECRET_KEY'] = b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'
app.config['MAIL_PASSWORD'] = 'Summer1793$'
app.config['MAIL_USERNAME'] = 'askflask388j@gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'askflask388j@gmail.com'
app.config['DEBUG'] = True
app.config['TESTING'] = False



mail = Mail(app)
# mongo = PyMongo(app)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'loginpage.login'
bcrypt = Bcrypt(app)
from askflask.homepage.routes import homepage
from askflask.loginpage.routes import loginpage
from askflask.questionpage.routes import questionpage

app.register_blueprint(homepage)
app.register_blueprint(loginpage)
app.register_blueprint(questionpage)
Talisman(
    app, 
    content_security_policy=csp,
)

