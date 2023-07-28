
from app import app, CURR_USER_KEY
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

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    def SetUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        self.testuser = User.signup(
            username='testusername', email='test@email.com', password='password123', image_url=None)
        self.testuser_id = 4566
        self.testuser.id = self.testuser_id
        self.user1 = User.signup(
            'testusername1', 'test1@email.com', 'password123', None)
        self.user2 = User.signup(
            'testusername2', 'test2@email.com', 'password123', None)
        self.user1_id = 122
        self.user2_id = 211
        self.user1.id = self.user1_id
        self.user2.id = self.user2_id
        db.session.commit()

    def test_user_display(self):
        with self.client as c:
            res = c.get(f'/users/{self.testuser_id}')
            self.AssertEqual(res.status_code, 200)
            self.AssertIn('@testusername')
