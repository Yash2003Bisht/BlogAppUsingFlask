from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from website.helper_functions import send_mail
from website.models import UserData
import re
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import current_user, login_required, login_user, logout_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = UserData.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("routes.index"))
            else:
                flash("Incorrect password", category="danger")
        else:
            flash("Invalid email", category="danger")
    return render_template("login.html", action="/login", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        if UserData.query.filter_by(email=email).first():
            flash("Email already exists", category="danger")
        elif len(name) < 3:
            flash("Invalid name!", category="danger")
        elif not bool(re.search(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9]*\.[a-zA-Z]{1,3}$", email)):
            flash("Invalid email!", category="danger")
        elif len(password) < 8:
            flash("Your password must be at least 8 characters", category="danger")
        elif password != confirmpassword:
            flash("Password don't match", category="danger")
        else:
            user_data = UserData(name=name, email=email, password=generate_password_hash(password, salt_length=12))
            db.session.add(user_data)
            db.session.commit()
            login_user(user_data, remember=True)
            return redirect(url_for("routes.index"))
    return render_template("signup.html", action="/sign-up")

@auth.route("/forget-password", methods=["GET", "POST"])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))
    elif request.method == "POST":
        user = UserData.query.filter_by(email = request.form["email"]).first()
        if not user:
            flash("Email not registered", category="danger")
        else:
            send_mail(user)
            flash("A link has been send to your email account", category="success")
    return render_template("forget_password.html", action = "/forget-password")

@auth.route("/forget-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))
        
    user = UserData.verify_token(token)
    if user is None:
        flash("That is invalid token or expired. Please try again.", category="danger")
        return redirect(url_for("auth.forget_password"))
    else:
        if request.method == "POST":
            password = request.form["password"]
            confirmpassword = request.form["confirmpassword"]
            if len(password) < 8:
                flash("Your password must be at least 8 characters", category="danger")
            elif password != confirmpassword:
                flash("Password don't match", category="danger")
            else:
                user.password = generate_password_hash(password, salt_length=12)
                db.session.commit()
                flash("Password change successfully", "success")
                return redirect(url_for("auth.login"))
        return render_template("add_new_password.html")

@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))