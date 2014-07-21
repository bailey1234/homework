#-*-coding:utf-8-*-
# all the imports
import json

import os
import re
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# create our little application :)
app = Flask(__name__) # 이름을 지정해야한다. 
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
 

@app.route('/login', methods=['GET','POST'])
def login(): # 같으면 로그인 
    message = None
    if request.method == 'POST':

        f = open('user.txt','r')
        data = f.read()
        f.close()
        users = json.loads(data)
        for user in users:                       
            if user['email']==request.form['username']:
                if user['password']==request.form['password']:
                    print "success"
                    return redirect(url_for('show_entries'))
                    
        else:
            
            message = 'try it again'
            return render_template('login.html',message=message)
    else:
        return render_template('login.html',message=message)



@app.route('/signup', methods=['GET','POST'])
def signup():
    message = None
    if request.method == 'POST':
        if request.form['email'] == "":
            message = 'email is empty'
        

        elif request.form['password'] == "":
            message = 'password is empty'

        else:
            if  bool(re.search("[\w\d._]+@[\w\d-]+\.(\w{2,3}|\w{2}\.\w{2})",request.form['email']))==True:
                message = 'email right'
                if bool(re.search("(?=.{8,20})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!#\$%&\?])",request.form['password']))==True:
                    message = 'password is right'
                    if request.form['password']==request.form['password_check']:
                        message= 'right~'
                        f = open('user.txt','r')
                        data = f.read()
                        f.close()
                        users = json.loads(data)

                        info={
                           "email" : request.form['email'],
                           "password" : request.form['password']
                        }
                        for user in users:
                            
                            if user['email'] ==request.form['email']:
                                message = 'error'
                                return render_template('signup.html', message=message)
                        users.append(info)

                        

                        f=open('user.txt','w')     
                        f.write(json.dumps(users))#loads
                        f.close() 

                       


                    elif request.form['password']!=request.form['password_check']:
                        message= 'not match'   
                elif not re.search("(?=.{8,20})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!#\$%&\?])",request.form['password']):
                    message= 'password error '       
            elif not re.search("[\w\d._]+@[\w\d-]+\.(\w{2,3}|\w{2}\.\w{2})",request.form['email']):
                message = 'email is wrong'
                if not re.search("(?=.{8,20})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!#\$%&\?])",request.form['password']):
                    message = 'password is wrong'
            else:
                message="hihi"
       

            
    return render_template('signup.html', message=message)    


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# 프로젝트 네임이름이 여러개일경우에 어떤걸 메인으로 하는 것 
# flask 
#
if __name__ == '__main__':
    app.run()    