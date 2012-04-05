# coding: utf-8

from tests import TestCase
from planlos.extensions import db
from planlos.documents import Group, DocumentExistsException, User, User_Exists_Exception
from planlos.passwordgen import Password_Generator
import bson
import re

class Test_Units(TestCase):

    def setUp(self):
        db.users.drop()
        #db.drop_collection("users")
        super(Test_Units,self).setUp()

    def test_create_group_allows_only_unique_names(self):
        self.login_as_moderator()
        oid = bson.objectid.ObjectId()
        g1 = db.Group.create(name=u'test1', desc=u'bla', members=[oid])
        self.assertRaises(DocumentExistsException,
                          db.Group.create,
                          name=u'test1',
                          desc=u'bla', members=[oid])

    def create_user(self, username):
        u = User.create( username=username, password=u'hallo',
                         signup_email=u'planlos-test1@localhost')

    def test_create_user(self):
        self.create_user(u'planlos-test1')
        from pymongo import Connection
        c = Connection()
        db = c.planlos_flask_test
        dbu= db.users.find_one({'username':u'planlos-test1'})
        self.assertNotEqual(dbu, None)

    def test_create_existing_user(self):
        self.create_user(u'testdouble')
        self.assertRaises(User_Exists_Exception, self.create_user, u'testdouble')

    def test_passwort_gen(self):
        p = Password_Generator(oldstyle=True)
        pw = p.gen()
        print pw
        assert(len(pw) == 10)
        p = Password_Generator()
        pw = p.gen()
        #re.compile(r'[a-z]')
        print pw
        assert(pw)
