from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from wtforms import ValidationError

    
class updateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class BlogForm(FlaskForm):    
    blogTitle = StringField('Blog Title',validators=[Required()])
    blogDescription = StringField('Description',validators = [Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment', validators=[Required()])
    submit = SubmitField('Submit')

class SubscriberForm(FlaskForm):
    email = StringField('Your Email Address')
    name = StringField('Enter your name',validators = [Required()])
    submit = SubmitField('Subscribe')
