from flask import Flask
from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify,render_template

app=Flask(__name__)

#设置这两个后，才能使用session
app.secret_key='djskla'
app.config['DEBUG']=True

# @app.route('/')
# def index():
#     return '<h1>Hello Flask I am wei ca-fafa gs</h1>'

# @app.route('/hi')
# @app.route('/hello')
# def say_hello():
#     return '<h1>This is say_hello</h1>'

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)

@app.route('/')
def index():
    return redirect(url_for('hello'))
    #return render_template('index.html')

#@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','Aolin')
    response = '<h1>Hello, %s!</h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response

@app.route('/login')
def login():
    session['logged_in']=True
    return redirect(url_for('hello'))

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

# @app.route('/login')
# def login():
#     session['logged_in'] = True
#     return redirect(url_for('hello'))



@app.route('/set/<name>')
def set_cookie(name):
    responst=make_response(redirect(url_for('hello')))
    responst.set_cookie('name',name)
    return responst


@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello,I am %s !</h1>' % name

if __name__=="__main__":
    app.run()