from flask import render_template,request,redirect,url_for,flash,abort
from . import main
from .. import db,photos
from flask_login import login_user,logout_user,login_required,current_user
from  requests import getQuotes
from .forms import BlogForm,CommentForm,updateProfile,SubscriberForm
from ..models import Blog,Comment,User,Subscriber
from ..email import mail_message

@main.route('/',methods = ['GET'])
def index():
    getquotes = getQuotes()
    return render_template ('index.html',getquotes = getquotes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()
    if user == None:
        abort(404)

    return render_template('profile/profile.html',user = user,blogs=blogs)  

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user == None:
        abort(404)

    form = updateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
           
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)  

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    

@main.route('/blog/newBlog',methods = ['GET','POST'])
@login_required
def newBlog():
    subscribers = Subscriber.query.all()
    blogForm = BlogForm()
    if blogForm.validate_on_submit():
        titleBlog=blogForm.blogTitle.data
        description = blogForm.blogDescription.data
        newBlog = Blog(title_blog=titleBlog, description=description, user= current_user)
        newBlog.saveBlog()
        for subscriber in subscribers:
            mail_message("Alert New Blog","email/newBlog",subscriber.email,newBlog=newBlog)
        return redirect(url_for('main.index'))
        flash('New Blog Posted')
        return redirect(url_for('main.allBlogs'))
    title = 'New Blog'
    return render_template('newBlog.html', title=title, blog_form=blogForm)


@main.route('/blog/allblogs', methods=['GET', 'POST'])
@login_required
def allBlogs():
    blogs = Blog.getallBlogs()
    return render_template('blogs.html', blogs=blogs)

@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def newComment(id):
    blog = Blog.query.filter_by(id = id).all()
    blogComments = Comment.query.filter_by(blog_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        new_comment = Comment(blog_id=id, comment=comment, user=current_user)
        new_comment.saveComment()
    return render_template('newComment.html', blog=blog, blog_comments=blogComments, comment_form=comment_form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteComment(id):
    comment =Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('comment succesfully deleted')
    return redirect (url_for('main.allBlogs'))


@main.route('/deleteblog/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteBlog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.allBlogs'))   


@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def updateBlog(id):
    blog = Blog.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title_blog = form.blogTitle.data
        blog.description = form.blogDescription.data
        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('main.allBlogs'))
    elif request.method == 'GET':
        form.blogTitle.data = blog.title_blog
        form.blogDescription.data = blog.description
    return render_template('updateBlog.html', form=form)

@main.route('/about')
def about():
    return render_template('about.html', title = 'About')  


@main.route('/subscribe', methods=['GET','POST'])
def subscriber():
    getquotes = getQuotes()
    subscriber_form=SubscriberForm()
    blog = Blog.query.order_by(Blog.posted.desc()).all()
    if subscriber_form.validate_on_submit():
        subscriber= Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)
        db.session.add(subscriber)
        db.session.commit()
        mail_message("Welcome to MyBlog","email/subscriber",subscriber.email,subscriber=subscriber)
        title= "MyBlog"
        return render_template('index.html',title=title, blog=blog, getquotes = getquotes)
    subscriber = Blog.query.all()
    blog = Blog.query.all()
    return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,blog=blog)  
