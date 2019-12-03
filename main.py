from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/newpost', methods=['POST','GET'])
def newblog():
    if request.method == 'POST':
        post_title = request.form['post_title']
        yourpost = request.form['yourpost']

    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        pass
       

    return render_template('blog.html')
if __name__ == '__main__':
    app.run()
