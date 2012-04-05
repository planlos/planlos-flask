# coding: utf-8

from tests import TestCase
from datetime import datetime,date,time
from planlos.documents import Event, User, Profile
from planlos.extensions import db
from planlos.views import accounts
from flask import url_for
import uuid


class TestUsers(TestCase):
    def test_create_user_and_login_without_activation(self):
        a = unicode(uuid.uuid1())
        p = db.Profile()
        u = User.create(username=u'test99',
                        password=u'test99',
                        signup_email=u'test@localhost',
                        activation_key=a,
                        )
        self.assertNotEqual(u, None)
        response = self.client.post("/users/login",
                                    data={'username': 'test99',
                                          'password': 'test99'})
        self.assert200(response)
        assert "Sorry, wrong credentials" in response.data

    def test_login(self):
        response = self.client.get("/users/login")
        self.assert_200(response)

    def test_logout(self):
        self.login_as_user()
        response = self.client.get("/users/logout")
        self.assert_200(response)

    def test_signup(self):
        response = self.client.get("/users/signup")
        self.assert_200(response)

    def test_index(self):
        response = self.client.get("/users/")
        self.assert_200(response)

    def test_login_user(self):
        response = self.client.post("/users/login",
                                    data={'username': u'test',
                                          'password': u'test'})
        self.assertRedirects(response, "/users/profile/%s" % 'test')
        #assert ( "Welcome test" in response.data)

    def test_signup_new_user(self):
        response = self.client.post("/users/signup",
                                    data={'username': u'user1',
                                          'password': u'test',
                                          'password2': u'test',
                                          'email': u'planlos-test2@localhost'},
                                    follow_redirects=True)
        self.assert_200(response)
        assert("Thanks for signing up" in response.data)
        assert("planlos-test2@localhost" in response.data)
        # second user should fail
        response = self.client.post("/users/signup",
                                    data={'username': u'user1',
                                          'password': u'test',
                                          'password2': u'test',
                                          'email': u'planlos-test2@localhost'})
        assert("Username is already taken" in response.data)
