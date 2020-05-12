# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash, Response, Blueprint
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from . import app, bcrypt, client
from .forms import (SearchForm, RegistrationForm, LoginForm, QuestionForm,
                             UpdateUsernameForm, UpdateProfilePicForm)
from .models import User, Question, load_user
from .utils import current_time

mod= Blueprint('account', __name__)
""" ************ View functions ************ """
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
 
    if form.validate_on_submit():
        return redirect(url_for('query_results', query=form.search_query.data))

    return render_template('index.html', form=form)

@app.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    results = client.search(query)

    if type(results) == dict:
        return render_template('query.html', error_msg=results['Error'])
    
    return render_template('query.html', results=results)

@app.route('/questionAsk', methods=['GET', 'POST'])
def newQuestionAsk():

    form = QuestionForm()
    
    if form.validate_on_submit():    
        questionContent=form.text.data
        if len(Question.objects(question_id=questionContent)) == 0:
      
            question = Question(
      
                commenter=load_user(current_user.username), 
                content=form.text.data, 
                date=current_time(),
                question_id=form.text.data,
             )
        
            question.save()

            return redirect(url_for('questionAsk', questionAsked=form.text.data))
        else:
            flash('Question Already Asked! Ask a different question!')
            #if you have time you could link em to the question
            return render_template('questionAsk.html', form=form)
    return render_template('questionAsk.html', form=form)

@app.route('/questionAsk/<questionAsked>', methods=['GET', 'POST'])
def questionAsk(questionAsked):
    
    if len(Question.objects(question_id=questionAsked)) == 0:
        return render_template('questionAsked.html', form=form, question=questionAsked)
    else:
        return render_template('questionAsked.html', form=form, question=questionAsked)

@app.route('/user/<username>')
def user_detail(username):
    user=load_user(username)
    if user is not None:
        return render_template('user_detail.html', user=username, reviews= Review.objects(commenter=user.id), total=len(Review.objects(commenter=user.id)))
    return render_template('user_detail.html')

"""
EXTRA CREDIT: Refer to the README
"""
@app.route('/images/<username>')
def images(username):
    pass


""" ************ User Management views ************ """
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        finalProjectUser = User(username=form.username.data, 
                    email=form.email.data, password=hashed)      
        finalProjectUser.save()
        flash('Please login')
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()  
   

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):              
            login_user(user)        
            return redirect(url_for('account'))
        else:
             flash('Wrong username or password.')
    return render_template('login.html', form=form)

 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    
    form = UpdateUsernameForm()
    
    if form.validate_on_submit():
        if len(User.objects(username=form.username.data)) == 0:  
            current_user.modify(username=form.username.data)
            current_user.save()
            return redirect(url_for('account'))           
        else:
            flash('This username is already taken!')                   
    return render_template('account.html', form=form, user=current_user)
