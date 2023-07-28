"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from models import db, User, Message, Follows
from sqlalchemy import exc

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        user1 = User.signup("testuser1", "test1@email.com",
                            "password123", None)
        uid1 = 1111
        user1.id = uid1
        user2 = User.signup("testuser2", "test2@email.com",
                            "password123", None)
        uid2 = 2222
        user2.id = uid2
        db.session.commit()
        user1 = User.query.get(uid1)
        user2 = User.query.get(uid2)
        self.user1 = user1
        self.user2 = user2
        self.uid1 = uid1
        self.uid2 = uid2

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_register_user(self):
        user = User.signup(
            'testusername', 'usertest@email.com', 'password123', None)
        uid = 3333
        user.id = uid
        db.session.commit()
        user = User.query.get(uid)
        self.assertEqual(user.username, 'testusername')
        self.assertEqual(user.email, 'usertest@email.com')
        self.assertNotEqual(user.password, 'password123')

    def test_register_invalid_email(self):
        user2 = User.signup('testuser', None, 'password123', none)
        uid = 1234
        user2.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
