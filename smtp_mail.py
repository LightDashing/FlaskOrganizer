from flask_mail import Message, Mail
from flask import render_template

class Email:

    def __init__(self, app):
        self.mail = Mail(app)

    def send_email(self, subject, sender, recipients, html_body, text_body):
        msg = Message(subject=subject, recipients=[recipients], sender=sender)
        msg.body = text_body
        msg.html = html_body
        self.mail.send(msg)

    def send_password_reset_email(self, token, user_id, email):
        self.send_email('[FlaskOrginizer] Reset Your Password',
                   sender='pythonsmtptester@gmail.com',
                   recipients=email,
                    text_body=render_template('reset_password.txt',
                                                  user_id=user_id, token=token),
                   html_body=render_template('reset_password.html',
                                             user_id=user_id, token=token))