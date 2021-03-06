from flask import Flask, render_template,redirect,url_for, request, session, flash
from functools import wraps 
from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3
from pprint import pprint

app = Flask(__name__)

#config
import os
app.config.from_object(os.environ['APP_SETTINGS'])
#print os.environ['APP_SETTINGS']
#create sqlalchemy object
db = SQLAlchemy(app)

from models import *

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('you need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
@login_required
def home():
    posts = []
    try:
        posts = db.session.query(Child).all()
        for child in posts:
            child.parent_id = 1
            flash('lol')
            flash(dir(child))
            flash(child.parent)
            flash(child.parent_id)
        return render_template("index.html",posts=[dict(title='ha', description='wat')])
    except:
        return render_template("index.html", posts=[dict(title='did not render', description='didnt render')])

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username'] != 'admin' or request.form['password']!='admin':
            error='Invalid credentials please try again'
        else:
            session['logged_in']=True
            flash('you were just logged in')
            return redirect(url_for('home'))
    return render_template('login.html',error=error)


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in',None)
    flash("You were just logged out")
    return redirect(url_for('welcome'))

#def connect_db():
#    return sqlite3.connect('posts.db')

if __name__ == "__main__":
    app.run()