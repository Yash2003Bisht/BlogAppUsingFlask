from math import ceil
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.models import UserData, UserPosts
from . import db
from datetime import datetime
from website.helper_functions import *

routes = Blueprint("routes", __name__)

@routes.route("/")
@login_required
def index():
    loadUserData()
    post_details = UserPosts.query.all()[::-1]
    last_page = ceil(len(post_details) / 5)

    # getting page number
    page_number = request.args.get("page")
    if page_number is None or len(page_number) == 0:
        page_number = 1
    page_number = int(page_number)

     # pagination logic starts
    if last_page == 1:
        previous = "#"
        next = "/?page=#"
    elif page_number == 1:
        previous = "#"
        next = "/?page=" + str(page_number + 1)
    elif page_number == last_page:
        previous = "/?page=" + str(page_number - 1)
        next = "#"
    else:
        previous = "/?page=" + str(page_number - 1)
        next = "/?page=" + str(page_number + 1)

    # fetching 5 posts in per page_number
    post_details = post_details[(page_number - 1)*5:(page_number - 1)*5+5]
    user_names = UserData.query.all()
    
    return render_template("index.html", user = user_data, post_details = post_details, user_names = user_names, previous = previous, next = next, current_user = current_user)

@routes.route("/about")
@login_required
def about():
    loadUserData()
    return render_template("about.html", user = user_data)

@routes.route("/user", methods=["GET", "POST"])
@login_required
def user():
    loadUserData()
    if request.method == "POST":
        form_data = {"phone": request.form["phone"], "message": request.form["message"]}
        body = f"""
        phone: {form_data["phone"]}
        Messaage: {form_data["message"]}
        """
        send_mail(user_data["credential"].email, body=body)
        flash("Your message is send to your team.", category="success")
    return render_template("user.html", user = user_data)

@routes.route("/new", methods=["GET", "POST"])
@login_required
def addNewPost():
    loadUserData()
    if request.method == "POST" and current_user.is_authenticated:
        title = request.form["title"]
        sub_title = request.form["sub_title"]
        content = request.form["content"]
        user_posts = UserPosts(title=title, sub_title=sub_title, content=content, refrence_key = current_user.id)
        db.session.add(user_posts)
        db.session.commit()
        flash("Blog added successfully", category="success")
        return redirect(url_for("routes.user"))
    return render_template("add_post.html", user = user_data)

@routes.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    user_posts = UserPosts.query.filter_by(id=id).first()
    if current_user.id == user_posts.refrence_key:
        db.session.delete(user_posts)
        db.session.commit()
        flash("Blog deleted successfully", category="success")
    else:
        flash("Permission dined", category="danger")
    return redirect(url_for("routes.user"))

@routes.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    loadUserData()
    user_posts = UserPosts.query.filter_by(id=id).first()
    if current_user.id == user_posts.refrence_key:
        if request.method == "POST":
            user_posts.title = request.form["title"]
            user_posts.sub_title = request.form["sub_title"]
            user_posts.content = request.form["content"]
            user_posts.date_created = datetime.now().strftime("%B %d, %Y %I:%M %p")
            db.session.add(user_posts)
            db.session.commit()
            flash("Blog updated Successfully", category="success")
            return redirect(url_for("routes.user"))
        return render_template("update_post.html", user=user_data, user_posts=user_posts)
    else:
        flash("Permission dined", category="danger")
        return redirect(url_for("routes.user"))

@routes.route("/post/<int:id>")
@login_required
def post(id):
    loadUserData()
    post_details = UserPosts.query.filter_by(id=id).first()
    user_name = UserData.query.filter_by(id=post_details.refrence_key).first()
    return render_template("post.html", user = user_data , post_details = post_details, user_name = user_name, current_user=current_user)


@routes.route("/user-profile/<int:id>")
@login_required
def user_profile(id):
    loadUserData()
    user_profile = UserData.query.filter_by(id=id).first()
    user_posts = UserPosts.query.filter_by(refrence_key=id).all()
    print(len(user_posts))
    return render_template("user_profile.html", user=user_data, user_profile=user_profile, user_posts=user_posts)