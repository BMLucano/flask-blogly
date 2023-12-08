"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

###User routes###

@app.get("/")
def home_page():
    """Redirects to list of users"""

    return redirect("/users")

@app.get("/users")
def show_user_list():
    """Show a list of all users and button to add a user"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.get("/users/new")
def show_create_user():
    """Show form to create a new user."""

    return render_template("create_user.html")

@app.post('/users/new')
def handle_create_user():
    """Handle create user form and add new user to database.
    Redirect to user list.
    """

    new_user = User(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        image_url = (request.form["image_url"]
                     if request.form["image_url"] else None)
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show details about a user with buttons to edit or delete profile."""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show form to edit a user's profile, with buttons to confirm or cancel"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.post("/users/<int:user_id>/edit")
def handle_edit_user(user_id):
    """Edits user's data in the database then redirects to /users"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = (request.form["image_url"]
                      if request.form["image_url"] else DEFAULT_IMAGE_URL)
    # import default image

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:user_id>/delete")
def handle_delete_user(user_id):
    """Removes user's posts, then user's info from the database
    then redirects to /users"""

    user = User.query.get_or_404(user_id)
    # user_posts = user.posts

    #would this be better off as a for in loop..what are the conventions
    [db.session.delete(post) for post in user.posts]
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

###Post routes###
@app.get("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """Show form for new post"""

    user = User.query.get_or_404(user_id)
    return render_template("create_post.html", user=user)

@app.post("/users/<int:user_id>/posts/new")
def handle_post_form(user_id):
    """Handle new post form. Add post to DB and redirect to user detail page"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form["title"],
                    content=request.form["content"],
                    user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    #flash message to show redirect..
    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def show_post(post_id):
    """Show post with options to edit and delete"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.get("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Show form to edit a post with option to cancel"""

    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.post("/posts/<int:post_id>/edit")
def handle_edit_post(post_id):
    """Handle edit post form. Update DB. Redirect to post details"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete post from DB. Redirect to user detail page"""

    post = Post.query.get_or_404(post_id)

    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")



