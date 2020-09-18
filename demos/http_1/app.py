import os
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify,json

app = Flask(__name__)

app.secret_key='nihaondfadsfad'
# @app.route('/hello')
# def hello():
#     name=request.args.get('name','Flask')
#     return '<h1>Hello,%s </h1>' %name

@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>'%(2020-year)

# @app.route('/hello')
# def hello():
#     return redirect('http://www.baidu.com')

@app.route('/hi')
def hi():
    return redirect(url_for('hello'))

@app.route('/404')
def not_found():
    abort(404)

# @app.route('/foo')
# def foo():
#     return jsonify(name='WeiWei',gender='male')
#     # data={
#     #     'name':'Grey Li',
#     #     'gender':'male'
#     # }
#     # response=make_response(json.dumps(data))
#     # response.mimetype='application/json'
#     # return response

@app.route('/set/<name>')
def set_cookie(name):
    response=make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response

@app.route('/')
@app.route('/hello')
def hello():
    name=request.args.get('name')
    if name is None:
        name=request.cookies.get('name','Human')
        response='<h1>Hello,%s</h1>' %name

        if 'login' in session:
            response+='[Authenticated]'
        else:
            response+='[Not Authenticated]'
        return response
    # name=request.args.get('name')
    # if name is None:
    #     name=request.cookies.get('name','Human')
    # return '<h1>Hello,%s</h1>' %name

@app.route('/login')
def login():
    session['login']=True
    return redirect(url_for('hello'))


@app.route('/admin')
def admin():
    if 'login' not in session:
        abort(403)
    return "Welcome to admin page"

@app.route('/logout')
def logout():
    if 'login' in session:
        session.pop('login')
    return redirect(url_for('hello'))

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something </a>' % url_for('do_something')

# @app.route('/foo')
# def foo():
#     return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
#            % url_for('do_something', next=request.full_path)
#
#
# @app.route('/bar')
# def bar():
#     return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
#            % url_for('do_something', next=request.full_path)

@app.route('/do_something')
def do_something():
    print(request.referrer)
    return redirect(request.referrer)
    #return redirect(url_for('hello'))

if __name__=="__main__":
    app.run()