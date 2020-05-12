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
from datetime import datetime

# local
from .. import app, bcrypt, client, mail
from .forms import (QuestionForm, QuestionAnsweredForm, LikeForm)
from ..models import User, Question, load_user, Answers, LikedPosts
from ..utils import current_time

questionpage=Blueprint('questionpage', __name__)

@questionpage.route('/questionAsk', methods=['GET', 'POST'])
@login_required
def questionAsk():

    form = QuestionForm()
    
    if form.validate_on_submit():    
        questionContent=form.text.data
        
        if len(Question.objects(question_id=questionContent)) == 0:
            
            question = Question(
      
                commenter=load_user(current_user.username), 
                content=questionContent, 
                date=current_time(),
                question_id=form.text.data,
                likes=0,
             )
        
            question.save()

            return redirect(url_for('questionpage.questionAnswered', questionAsked=form.text.data))
        else:
            flash('Question Already Asked! Ask a different question or click here to view the question\'s page!')
            #if you have time you could link em to the question
            
            return render_template('questionAsk.html', form=form, question=questionContent)
    return render_template('questionAsk.html', form=form)

@questionpage.route('/questionAnswered/<questionAsked>', methods=['GET', 'POST'])
def questionAnswered(questionAsked):
   
    form= QuestionAnsweredForm()
    if form.validate_on_submit(): 
      
        answer = Answers(  
            answer=form.text.data,
            date=current_time(),
            question_id=questionAsked,
            commenter=load_user(current_user.username), 
         
        )
        username= Question.objects(question_id=questionAsked).first().commenter
       
        if(current_user.username != username.username):
         
            username= Question.objects(question_id=questionAsked).first().commenter
           
            msg = Message("Someone answered your question!",
                 recipients=username.email.split())
            
            msg.body = current_user.username+" answered your question!"
            mail.send(msg)
        
        answer.save()

        return redirect(url_for('questionpage.questionAnswered', questionAsked=questionAsked))
    form1= LikeForm()
    if form1.validate_on_submit():
        y=0
        qu=Question.objects(question_id=questionAsked)
      
        if qu.first().likes!=0:
            lp=LikedPosts.objects()
            for i in range(len(LikedPosts.objects())):
                x= lp.next()
            
               
          
            
                if x.question_id == questionAsked and current_user.username == x.liker:
                     y=1
                    
        if y==0:
            thisliker=LikedPosts(
                liker=current_user.username,
                question_id=questionAsked,
            )
            thisliker.save()
         
            prevLikes=Question.objects(question_id=questionAsked).first().likes
            numOfLikes=Question.objects(question_id=questionAsked).first().modify(likes=prevLikes+1)
           
        return redirect(url_for('questionpage.questionAnswered', questionAsked=questionAsked))
    answers = Answers.objects(question_id=questionAsked)
   
    return render_template('questionAnswered.html', form=form, form1=form1, question=questionAsked,numlikes=Question.objects(question_id=questionAsked).first().likes, answers=answers)

@questionpage.route('/allQuestions', methods=['GET', 'POST'])
def allQuestions():
    arr=[]
    for i in Question.objects():
        arr.append(i)
    arr.sort(key=lambda x: x.likes, reverse=True)
    return render_template('allQuestions.html', questions=arr)


