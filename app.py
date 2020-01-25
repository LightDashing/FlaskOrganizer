from flask import Flask, render_template, request, redirect, url_for
from database import DBWork

app = Flask(__name__)

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
            return render_template('index.html', error="passwords_dont_match")
        db = DBWork()
        if not db.user_add(name, email, password):
            return render_template('index.html', error='already_exist')
        db.close()
        return redirect(url_for('users_page', name=name))

        #return 'Thanks'

@app.route('/users/<name>')
def users_page(name):
    return render_template('user.html', name=name.title())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pw1']
        db = DBWork()
        if not db.user_login(email, password):
            pass

app.run(debug=True)
