from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)




class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Search')
