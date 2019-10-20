from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

def title_error(blog_title):
    if len(blog_title) > 0:
        return False
    else:
        return True

def body_error(blog_body):
    if len(blog_body) > 0:
        return False
    else:
        return True

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180))
    body =db.Column(db.String(4000))

    #completed = db.Column(db.Boolean)
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    blog_id =str(request.args.get('id'))
    blogs = Blog.query.all()       
    myentry = Blog.query.get(blog_id)   
    return render_template('blogs.html', blogs=blogs, myentry=myentry)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error_msg = ''
        body_error_msg = ''

        if title_error(blog_title):
            title_error_msg = "Please enter a blog title."
            return render_template('/newpost.html', title_error=title_error_msg, body_error=body_error_msg, blog_body=blog_body)

        if body_error(blog_body):
            body_error_msg = "Please enter your thoughts -- how else will you make a blog post?"
            return render_template('/newpost.html', title_error=title_error_msg, body_error=body_error_msg, blog_title=blog_title)

        else:
            newpost = Blog(blog_title, blog_body)
            db.session.add(newpost)
            db.session.commit()
            return redirect('/?id=' + str(newpost.id))

    else:
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()