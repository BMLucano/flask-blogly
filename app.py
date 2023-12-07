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
        image_url = request.form["image_url"]
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show details about a user with buttons to edit or delete profile."""
    user = User.query.get(user_id)
    return render_template("user_detail.html", user=user)
