from . import db, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as serializer

class UserData(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(120))
    posts = db.relationship('UserPosts')

    def get_token(self, expires_sec = 900):
        serial = serializer(app.config["SECRET_KEY"], expires_in=expires_sec)
        return serial.dumps({"user_id": self.id}).decode("utf-8")
    
    @staticmethod
    def verify_token(token):
        serial = serializer(app.config["SECRET_KEY"])
        try:
            user_id = serial.loads(token)["user_id"]
        except Exception:
            return None
        return UserData.query.get(user_id)


class UserPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(550))
    sub_title = db.Column(db.String(1050))
    date_created = db.Column(db.String(20), default=datetime.now().strftime("%B %d, %Y %I:%M %p"))
    content = db.Column(db.String(10000))
    refrence_key = db.Column(db.Integer, db.ForeignKey('user_data.id'))

