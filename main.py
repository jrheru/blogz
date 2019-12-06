from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(999))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')


@app.route('/blog', methods=['GET','POST'])
def blog():
    if request.args:
        blog_id = request.args.get('id')
        if (blog_id):
            post = Blog.query.get(blog_id)
            return render_template('single_entry.html', title='Build a Blog', post=post)
        

    else:
        all_blogs = Blog.query.all()
        return render_template('blog.html', title='Build a Blog', blogs=all_blogs)

    # return render_template('blog.html')
       




@app.route('/newpost', methods=['POST','GET'])
def newblog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)

        title_error = ''
        body_error = ''

        if len(blog_title) == 0:
            title_error = 'Please enter a title!'

        if len(blog_body) == 0:
            body_error = 'Please tell us something!'

        if not title_error and not body_error:
            db.session.add(new_blog)
            db.session.commit()

            post_link = "/blog?id=" + str(new_blog.id)
       
            return redirect(post_link)
        else:
            return render_template('newpost.html', title="Create a Blog",
         blog_title=blog_title, title_error=title_error,
          blog_body=blog_body, body_error=body_error)

    else:
        return render_template('newpost.html', title='Create a Blog')
        
        
        

    

if __name__ == '__main__':
    app.run()
