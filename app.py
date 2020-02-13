from flask import Flask, render_template, request, redirect, url_for, session
from database import DBWork
from smtp_mail import Email
from flask_mail import Message, Mail
import jwt
from time import time

app = Flask(__name__)
app.secret_key = 'SomeSuperDuperSecretKey'
app.config['SECRET_KEY'] = 'SomeSuperDuperSecretKey'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pythonsmtptester@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'pythonsmtptester@gmail.com'
app.config['MAIL_PASSWORD'] = '***REMOVED***'
email_app = Email(app)

def get_reset_password_token(user_id, expires_in=600):
    return jwt.encode({'reset_password': user_id, 'exp':time() + expires_in}, app.secret_key, algorithm='HS256').decode('utf-8')

def veryfy_reset_password_token(token):
    try:
        id = jwt.decode(token, app.secret_key, algorithms=['HS256'])['reset_password']
    except:
        return
    return id

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', error=None)
    else:
        email = request.form['email']
        name = request.form['username']
        password = request.form['pw1']
        password_check = request.form['pw2']
        if password != password_check:
            db.session.close()
            return render_template('index.html', error="passwords_dont_match")
        db = DBWork()
        if not db.user_add(name, email, password):
            db.session.close()
            return render_template('index.html', error='already_exist')
        db.session.close()
        session['username'] = name
        return redirect(url_for('users_page', name=name))


@app.route('/users/<name>', methods=['GET', 'POST'])
def users_page(name):
    db = DBWork()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['description']
        end_date = request.form['end_date']
        db.task_add(title=title, description=content, deadline=end_date, user_id=db.get_user_data(name).id)
    user_tasks = db.tasks_get(name)
    db.session.close()
    return render_template('user.html', name=name, tasks=user_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pw1']
        db = DBWork()
        if not db.user_login(email, password):
            db.close()
            return render_template('login.html', error='dont_match')
        user_name = db.get_user_nickname(email)
        session['username'] = user_name
        db.session.close()
        return redirect(url_for('users_page', name=user_name))
    else:
        return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/delete/task_<task_id>')
def delete_task(task_id):
    db = DBWork()
    db.task_delete(int(task_id), session['username'])
    db.session.close()
    return redirect(url_for('users_page', name=session['username']))

@app.route('/complete/task_<task_id>')
def complete_task(task_id):
    db = DBWork()
    db.task_chstatus(int(task_id), session['username'])
    db.session.close()
    return redirect(url_for('users_page', name=session['username']))

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        db = DBWork()
        email = request.form['email']
        id = db.get_user_data(db.get_user_nickname(email)).id
        token = get_reset_password_token(id)
        email_app.send_password_reset_email(token=token, user_id=id, email=email)
        return render_template('reset.html')
    else:
        return render_template('reset.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    db = DBWork()
    user_id = veryfy_reset_password_token(token)
    if not user_id:
        return render_template('404.html')
    if request.method == 'POST':
        new_password = request.form['pw']
        db.change_user_password(user_id, db.password_crypter(new_password))
        db.session.close()
        return render_template('index.html')
    else:
        return render_template('password_change.html')


app.run(debug=True)
