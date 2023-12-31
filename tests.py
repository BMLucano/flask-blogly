import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase
from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post




# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.

        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    ### tests for users
    def test_list_users(self):
        """Test that user list displays and shows user"""

        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_create_user(self):
        """Test that new user gets added to user list and request redirects"""

        with app.test_client() as c:
            d = {"first_name": "test2_first",
                 "last_name": "test2_last",
                 "image_url": "w"}
            resp = c.post("/users/new", data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("test2_first", html)
            self.assertIn("test2_last", html)

    def test_delete_user(self):
        """Test that user is deleted and request redirects"""

        with app.test_client() as c:
            resp = c.post(f"/users/{self.user_id}/delete",
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)

    def test_show_edit_form(self):
        """Test that edit form displays"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("<h1>Edit a user</h1>", html)

    def test_edit_user(self):
        """Test that user is edited and request redirects."""

        with app.test_client() as c:
            d = {"first_name": "test1_edited_first",
                 "last_name": "test1_edited_last", "image_url": "w"}
            resp = c.post(f"/users/{self.user_id}/edit",
                          data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("test1_edited_first", html)
            self.assertIn("test1_edited_last", html)

    def test_show_user_details(self):
        """Test that user details display"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("<h1> test1_first test1_last</h1>", html)
            self.assertIn("test1_title</a></li>", html)



class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.

        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    ### tests for posts###
    def test_show_post(self):
        """Test that post displays"""

        with app.test_client() as c:
            resp = c.get(f"/posts/{self.post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("<h1>test1_title</h1>", html)
            self.assertIn("test1_content", html)

    def test_create_post(self):
        """Test that new post gets added to post list
        in user details and request redirects"""

        with app.test_client() as c:
            d = {"title": "test2_title",
                 "content": "test2_content",
                 "user_id": self.user_id}
            resp = c.post(f"/users/{self.user_id}/posts/new",
                          data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("test2_title", html)

    def test_edit_post(self):
        """Test that post is edited and request redirects"""

        with app.test_client() as c:
            d = {"title": "test1_title_edited",
                 "content": "test1_content_edited",
                 "user_id": self.user_id}
            resp = c.post(f"/posts/{self.post_id}/edit",
                          data=d,
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("<h1>test1_title_edited</h1>", html)
            self.assertIn("test1_content_edited", html)

    def test_delete_post(self):
        """Test that post is deleted and request redirects"""

        with app.test_client() as c:
            resp = c.post(f"/posts/{self.post_id}/delete",follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertNotIn("test1_title", html)