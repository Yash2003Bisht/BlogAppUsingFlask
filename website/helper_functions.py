from flask import url_for
from flask_login import current_user
from website.models import UserData, UserPosts
from flask_mail import Mail
from random import randrange
from . import app


user_data = {}

def loadUserData():
    global user_data
    user_data.update({"credential": UserData.query.filter_by(id=current_user.id).first(), "posts": UserPosts.query.filter_by(refrence_key=current_user.id).all()})

# Enable less secure apps
def send_mail(user, body=None):
    app.config.update(
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_USE_SSL = True,
        MAIL_PORT = "465",
        MAIL_USERNAME = "Enter Your Email",
        MAIL_PASSWORD = "Enter Your Password"
    )
    mail = Mail(app)
    if body is None:
        token = user.get_token()
        mail.send_message(
            "Forgot Password Request",
            body=f"""
            To reset yout password. Please click on this link: {url_for("auth.reset_password", token=token, _external=True)}

            This link valid for next 15 minutes
            """,
            recipients = [user.email],
            sender = "faltuhello1234@gmail.com"
        )
    else:
        mail.send_message(f"User Send Message {user}", body=body, sender=user, recipients = ["faltuhello1234@gmail.com"])


