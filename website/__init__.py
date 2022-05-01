from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os.path import exists
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)

def index():
    app.config["SECRET_KEY"] = "wertyuiojhgfdcx54d54a5s#$%^&*gadv"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)
    from .routes import routes
    from .auth import auth
    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    from .models import UserData, UserPosts
    createDataBase(app)
    lm = LoginManager()
    lm.login_view = "auth.login"
    lm.init_app(app)

    @lm.user_loader
    def load_user(id):
        return UserData.query.get(int(id))

    return app

def createDataBase(app):
    if not exists("website/database.db"):
        db.create_all(app=app)
