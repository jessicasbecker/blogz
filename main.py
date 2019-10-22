#blogz
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/index', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/')
def mainpage():
    return render_template('index.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blogs', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/index')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            #session is a flask element that will remember the user across other pages
            session['email'] = email
            flash("Logged in")
            return redirect('/index')
        else:
            flash("User password is incorrect or user does not exist. Pls try again.", "error")
            
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/index')
        else:
            return '<h1>Duplicate User!</h1>'

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/index')


@app.route('/blogs', methods=['POST', 'GET'])
def blog_display():
    user_id =str(request.args.get('user'))
    owner = Blog.query.filter_by(id=user_id).first()

    blog_id =str(request.args.get('id'))
    blogs = Blog.query.filter_by(owner=owner).all()
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
            owner = User.query.filter_by(email=session['email']).first()
            newpost = Blog(blog_title, blog_body, owner)
            db.session.add(newpost)
            db.session.commit()
            return redirect('blogs?id=' + str(newpost.id))

    else:
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()