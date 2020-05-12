from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
import pyotp


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    otp_secret = db.StringField(default=pyotp.random_base32(), required=True, min_length=16, max_length=16)
    email=db.EmailField(unique=True, required=True)
    username=db.StringField(unique=True, required=True, min_length=1, max_length=40)
    password=db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Question(db.Document):
    commenter=db.ReferenceField(User, required=True)
    content=db.StringField(required=True, min_length=0, max_length=500)
    date=db.StringField(required=True)
    question_id=db.StringField(required=True,min_length=0, max_length=500)
    likes=db.IntField(required=True, min_length=0)
    
    
class Answers(db.Document):
    commenter=db.ReferenceField(User, required=True)
    answer=db.StringField(required=True, min_length=0, max_length=500)
    date=db.StringField(required=True)
    question_id=db.StringField(required=True,min_length=0, max_length=500)

class LikedPosts(db.Document):
    liker=db.StringField(required=True,min_length=0, max_length=500)
    question_id=db.StringField(required=True,min_length=0, max_length=500)
 