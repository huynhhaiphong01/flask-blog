"""
Routes and views for the flask application.
"""

from datetime import datetime
from FinalProjectPython import app,models

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BLOG.db'

db = SQLAlchemy(app)
models.user = "failed"
models.id = 0
class Blogpost(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String())
    content = db.Column(db.Text)
    idpost = db.Column(db.Integer)
    date = db.Column(db.DateTime)

class User(db.Model):
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())
    fullname = db.Column(db.String())
    numberphone = db.Column(db.String())
    gmail = db.Column(db.String())
    note = db.Column(db.String())

@app.route('/',methods=['POST', 'GET'])
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    if request.method == 'POST':
        name = request.form['username']
        pw = request.form['password']
        user = User.query.filter_by(username=name, password = pw).first()
        if user is None:
            return render_template('login.html',error = "yes")
        else:
            models.user = user.fullname
            models.id = user.username
            return render_template('index.html', posts=posts, user = user.fullname)
    if models.user == "failed":
        return render_template('index.html', posts=posts)
    return render_template('index.html', posts=posts,user=models.user)



   

@app.route('/login')
def login():
    models.user = "failed"
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/registersuccess', methods=['POST'])
def registersuccess():
    name = request.form['username']
    pw = request.form['password']
    cpw = request.form['confirmpassword']
    if pw != cpw:
        return render_template('register.html',error = "yes")
    fname = request.form['fullname']
    user = User(username = name,password = pw,fullname = fname)
    try:
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    except:
        return render_template('register.html',error = "yes")


@app.route('/about')
def about():
    if models.user == "failed":
        return render_template('about.html') 
    return render_template('about.html',user=models.user)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    cmt = Comment.query.filter_by(idpost=post_id)
    if models.user == "failed":
        return render_template('post.html', post=post,cmts = cmt) 
    if models.user == post.author:
        return render_template('post.html', post=post,user=models.user,admin="yes",cmts = cmt) 
    return render_template('post.html', post=post,user=models.user,cmts = cmt) 

@app.route('/profile')
def profile():
    user = User.query.filter_by(username = models.id).first()
    count = Blogpost.query.filter_by(author=models.user).count()
    return render_template('profile.html', user=user, count = count)

@app.route('/updateprofile/',methods=['POST'])
def updateprofile():
    user = User.query.filter_by(username = models.id).first()
    user.gmail = request.form['gmail']
    user.numberphone = request.form['phone']
    user.note = request.form['note']
    db.session.commit()
    return redirect(url_for('profile'))
    

@app.route('/update/<int:post_id>')
def update(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    if models.user == "failed":
        return render_template('update.html', post=post) 
    return render_template('update.html', post=post,user=models.user) 

@app.route('/add')
def add():
    #if models.user == "failed":
     #   return render_template('add.html', posts = posts) 
    return render_template('add.html',user=models.user)

@app.route('/addpost/', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/addcomment/<int:post_id>', methods=['POST'])
def addcomment(post_id):
    content = request.form['content']
    comment = Comment(author = models.user,content = content, idpost = post_id, date=datetime.now())
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('post',post_id=post_id))


@app.route('/updatepost/<int:post_id>', methods=['POST'])
def updatepost(post_id):
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']
    post = Blogpost.query.filter_by(id=post_id).one()
    post.title = title
    post.subtitle = subtitle
    post.content = content
    db.session.commit()
    return redirect(url_for('post',post_id=post_id))

@app.route('/deletepost/<int:post_id>')
def deletepost(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)