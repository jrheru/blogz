from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'abcd'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(99), unique=True)
    pw_hash = db.Column(db.String(99))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

class Blog(db.Model):

    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(99))
    body = db.Column(db.String(999))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash('logged in')
            return redirect('/newpost')

        else:
            flash('User password incorrect, or user does not exist', 'error' )
            return redirect('/login')

    # else:
    #     return render_template('login.html', title='Blogz Login')
            
            

    


@app.route('/signup', methods=['POST','GET'])
def signup():
     if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         verify = request.form['verify']
         
         if username == '':
             flash('enter a username')
             return redirect('/signup')
         if len(username) <= 3:
             flash('invalid username')
             return redirect('/signup')
         if password == '':
             flash('enter a password')
             return redirect('/signup')
         if len(password) <= 3:
             flash('invalid password')
             return redirect('/signup')
         if password != verify:
             flash('passwords did not match')
             return redirect('/signup')
         user_db_count = User.query.filter_by(username=username).count()
         if user_db_count > 0:
             flash('username already taken')
             return redirect('/signup')
         user = User(username=username, password=password)
         db.session.add(user)
         db.session.commit()
         session['user'] = user.username
         return redirect('/newpost')
     else:
         return render_template('signup.html', title='Blogz Signup')



@app.route('/newpost', methods=['POST','GET'])
def newblog():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body, owner)

        title_error = ''
        body_error = ''

        if len(blog_title) == 0:
            title_error = 'Please enter a title!'

        if len(blog_body) == 0:
            body_error = 'Please tell us something!'

        if not title_error and not body_error:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_blog.id))

            # post_link = "/blog?id=" + str(new_blog.id)
       
            # return redirect(post_link)
        else:
            blogs = Blog.query.filter_by(owner=owner).all()
            return render_template('newpost.html', title="Create a Blog",
         blogs=blogs, blog_title=blog_title, title_error=title_error,
          blog_body=blog_body, body_error=body_error)

    else:
        return render_template('newpost.html', title='Create a Blog')


@app.route('/blog', methods=['GET','POST'])
def blog():
    posts = Blog.query.all()
    blog_id = request.args.get('id')
    user_id = request.args.get('user')

    if user_id:
        posts = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', posts=posts, title='User Post')
    if blog_id:
        post = Blog.query.get(blog_id)
        return render_template('entry.html', post=post)

    return render_template('blog.html', posts=posts, title='All Blog Post')

    

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')



@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', title='Blogz', users=users)


        
        

    

if __name__ == '__main__':
    app.run()
