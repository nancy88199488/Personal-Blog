from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255)) 
    blog = db.relationship('Blog', backref='user',passive_deletes=True,lazy="dynamic")   
    comment = db.relationship('Comment', backref='user',passive_deletes=True,lazy="dynamic")
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'User {self.username}'


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    title_blog = db.Column(db.String(255), index=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    def saveBlog(self):
        db.session.add(self)
        db.session.commit()

    def deleteBlog(self):
        db.session.delete(self)
        db.session.commit()  
    @classmethod
    def getBlogs(cls, id):
        blogs = Blog.query.filter_by(id=id).all()
        return blogs
    @classmethod
    def getallBlogs(cls):
        blogs = Blog.query.all()
        return blogs
    
    def __repr__(self):
        return f'Blogs {self.blog_title}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id',ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    def saveComment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def getComment(cls, blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return comments
    def deleteComment(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'Comments: {self.comment}'

class Subscriber(UserMixin, db.Model):
   __tablename__="subscribers"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255))
   email = db.Column(db.String(255),unique = True,index = True)
   def save_subscriber(self):
       db.session.add(self)
       db.session.commit()
   @classmethod
   def get_subscribers(cls,id):
       return Subscriber.query.all()
   def __repr__(self):
       return f'User {self.email}'
      
