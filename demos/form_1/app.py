import os
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from flask_ckeditor import CKEditor, upload_success, upload_fail
from flask_dropzone import Dropzone
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

from forms import LoginForm

app = Flask(__name__)

#设置这两个后，才能使用session
app.secret_key='djskla'
app.config['DEBUG']=True

app.secret_key = 'wwwwww'

@app.route('/html', methods=['GET', 'POST'])
def html():
    form = LoginForm()
    print("form.username() :",form.username())
    print("form.username.label() : ",form.username.label())
    print("form.submit.label() :",form.submit.label())

    print("form.submit(): ",form.submit())


    if request.method == 'POST':
        username = request.form.get('username')
        #flash('Welcome home, %s!' % username)
        password=request.form.get('password')
        flash('Welcom home ,%s ,your password is %s '%(username,password))
        print("===================")
        print(username,password)
        #return redirect(url_for('index'))
    return render_template('pure_html.html')


if __name__=="__main__":
    app.run()