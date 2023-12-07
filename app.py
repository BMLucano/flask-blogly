"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

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
    return render_template("edit.html", user=user)

@app.post("/users/<int:user_id>/edit")
def handle_edit_user(user_id):
    """Edits user's data in the database then redirects to /users"""

    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = (request.form["image_url"]
                      if request.form["image_url"] else user.image_url)
    # import default image

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:user_id>/delete")
def handle_delete_user(user_id):
    """Removes user's info from the database then redirects to /users"""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")