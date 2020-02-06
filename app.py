from flask import Flask, render_template, request, redirect, url_for, session
from database import DBWork

app = Flask(__name__)
app.secret_key = 'SomeSuperDuperSecretKey'

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
            db.close()
            return render_template('index.html', error="passwords_dont_match")
        db = DBWork()
        if not db.user_add(name, email, password):
            db.close()
            return render_template('index.html', error='already_exist')
        db.close()
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
    db.close()
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
        db.close()
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
    db.close()
    return redirect(url_for('users_page', name=session['username']))

@app.route('/complete/task_<task_id>')
def complete_task(task_id):
    db = DBWork()
    db.task_chstatus(int(task_id), session['username'])
    db.close()
    return redirect(url_for('users_page', name=session['username']))

app.run(debug=True)
