import os
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify

app = Flask(__name__)

@app.route('/hello')
def hello():
    name=request.args.get('name','Flask')
    return '<h1>Hello,%s </h1>' %name

@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>'%(2020-year)



if __name__=="__main__":
    app.run()