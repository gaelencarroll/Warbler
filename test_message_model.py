from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Follows, Message, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.uid = 94566
        u = User.signup('testuser', 'testemail@test.com', 'password123', None)
        u.id = self.uid
        db.session.commit()
        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def test_messages(self):
        msg = Message(text='this is the tweet', user_id=self.uid)
        db.session.add(msg)
        db.session.commit()
        self.assertEqual(self.u.messages[0].text, 'this is the tweet')

    def test_likes(self):
        msg_1 = Message(text='this is the tweet', user_id=self.uid)
        msg_2 = Message(text='this is the other tweet', user_id=self.uid)
        u = User.signup('testuser2', 'testemail2@test.com',
                        'password321', None)
        uid = 888
        u.id = uid
        db.session.add_all([msg_1, msg_2, u])
        db.session.commit()
        u.likes.append(msg_1)
        db.session.commit()
        like = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(like), 1)
