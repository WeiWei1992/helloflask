# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import click
from flask import Flask,redirect,url_for,abort,make_response,jsonify
from flask import make_response,request,session
from urllib.parse import urlparse,urljoin
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)

#设置这两个后，才能使用session
app.secret_key='djskla'
app.config['DEBUG']=True


# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/post')
def show_post():
    post_body=generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script type="text/javascript"></script>
    $(function(){
        $('#load').click(function(){
            $.ajax({
                url:'/more',
                type:'get',
                success:function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>''' % post_body

@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

def is_safe_url(target):
    ref_url=urlparse(request.host_url)
    test_url=urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and ref_url.netloc ==test_url.netloc

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do somethding and redicrect</a>' %url_for('do_something',next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something',next=request.full_path)
def redirect_back(default='hello',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
        # if target:
        #     return redirect(target)
    return redirect(url_for(default,**kwargs))
@app.route('/do_something_and_redirect')
def do_something():
    return redirect_back()


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'

# bind multiple URL for one view function
#@app.route('/hi')
@app.route('/hello')
def hello():
    name=request.args.get('name')
    if name is None:
        name=request.cookies.get('name','Human')
        response='<h1>Hello, %s</h1>' % name
        if 'logged_in' in session:
            response  =response+'[Authertiacted]'
        else:
            response=response+'[Not Authertiated]'
        return response
    #return '<h1>Hello, %s</h1>' % name
    #return '<h1>Hello, Flask!</h1>'
    #return '<h1>haha</h1>'
    #return '',302,{'location','http://example.com'}
    #return redirect('https://www.baidu.com')
    #return '<h1>Hello,I am is hello!</h1>'

@app.route('/login')
def login():
    #app.config['SESSION_TYPE'] = 'filesystem'
    session['logged_in']=True
    return redirect(url_for('hello'))


@app.route('/hi')
def say_hi():
    return redirect(url_for('hello'))

@app.route('/404')
def no_found():
    abort(404)

# @app.route('/foo')
# def foo():
#     return jsonify({'name':'grey li','gender':'male'})
    # response=make_response("Hello,World")
    # response.mimetype='text/plain'
    # return response

@app.route('/set/<name>')
def set_cookie(name):
    response=make_response(redirect(url_for('say_hello')))
    response.set_cookie('name',name)
    return response


@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d</p>' % (2018-year)

# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# custom flask cli command
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')
