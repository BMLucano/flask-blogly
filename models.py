"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTx4ETXIMlUwZYiZuG1B8eLRTu-oDZmV4lW9tuIe3lmIA&s"

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User of the site

    Fields:
        id: primary key
        first_name: text, not null
        last_name: text, not null
        image_url: text, default=?
    """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(20),
        nullable=False
    )

    last_name = db.Column(
        db.String(20),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )


