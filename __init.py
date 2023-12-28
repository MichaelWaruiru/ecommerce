from flask_mail import Mail, Message
from threading import Thread
from flask import current_app

mail = Mail()


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)
        
        
def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email(), args=(current_app._get_current_object(), message)).start()
