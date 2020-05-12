from flask import render_template, request, redirect, url_for, flash, Response, Blueprint
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import random

# stdlib

# local
from datetime import datetime

# local
from .. import app, bcrypt, client
from .forms import (SearchForm)
from ..models import User, Question, load_user, Answers, LikedPosts
from ..utils import current_time


homepage= Blueprint('homepage', __name__)
""" ************ View functions ************ """

@homepage.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    qu=Question.objects()
    arr=[]
    arr1=[]
   
    for i in range(len(Question.objects())):
       arr.append(qu.next())
    for i in range(10):
        if len(arr) > 0:
            x=random.choice(arr)
            if x not in arr1:
                arr1.append(x)
            else:
                i=i-1
    if form.validate_on_submit():
        return redirect(url_for('homepage.question_results', question=form.search_query.data))
    arr1.sort(key=lambda x: x.likes, reverse=True)
    return render_template('index.html', form=form, questions=arr1)

@homepage.route('/search-results/<question>', methods=['GET'])
def question_results(question):

    results = Question.objects(content=question)

    if len(results) == 0:
        return render_template('query.html', error_msg='This question does not exit! Would you like to ask it? Click here!')
    
    return redirect(url_for('questionpage.questionAnswered', questionAsked=question))  

@homepage.route('/groupMembers', methods=['GET'])
def groupMembers(): 
    return render_template('groupMembers.html')