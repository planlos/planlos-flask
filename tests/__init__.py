from flask import g
from flaskext.testing import TestCase as Base, Twill
from planlos import create_app
from planlos.config import Testing
from planlos.extensions import db
from planlos.documents import User, Event, Group
import uuid


class TestCase(Base):
    def create_app(self):
        app = create_app(Testing())
        self.twill = Twill(app)
        return app

    def setUp(self):
        # clean DB
        db.users.drop()
        db.events.drop()
        db.groups.drop()

        # create normal user
        a = unicode(uuid.uuid1())
        u = User.create(username=u'test',
                        password=u'test',
                        roles=[u'authenticated'],
                        signup_email=u'test@localhost',
                        activation_key=a,
                        active=True)
        #print u
        self.assertNotEqual(u, None)

        # create a moderator
        a = unicode(uuid.uuid1())
        u = User.create(username=u'mod',
                        password=u'mod',
                        roles=[u'authenticated', u'moderator'],
                        signup_email=u'mod@localhost',
                        activation_key=a,
                        active=True)
        #print u
        self.assertNotEqual(u, None)

        #g.identity = AnonymousIdentity()

    def tearDown(self):
        pass

    def assert_401(self, response):
        assert response.status_code == 401

    def login_as_user(self):
        data = { 'username' : 'test', 'password' : 'test' }
        response = self.client.post("/users/login", data=data, follow_redirects=True)

    def login_as_moderator(self):
        data = { 'username' : 'moderator', 'password' : 'moderator' }
        response = self.client.post("/users/login", data=data, follow_redirects=True)

    def login(self, **kwargs):
        response = self.client.post("/users/login/", data=kwargs)
        assert response.status_code in (301, 302)

    def logout(self):
        response = self.client.get("/users/logout/")
