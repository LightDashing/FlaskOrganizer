from flask import Flask, render_template, request, redirect, url_for
from database import DBWork

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('users.html')
    else:
        email = request.form['email']
        name = request.form['username']
        password = request.form['pw1']
        password_check = request.form['pw2']
        if password != password_check: return "Passwords don't match!"
        db = DBWork()
        db.user_add(name, email, password)
        db.commit()
        db.close()
        return redirect(url_for('users_page', name=name))

        #return 'Thanks'

@app.route('/users/<name>')
def users_page(name):
    return render_template('title.html', name=name.title())

app.run(debug=True)
