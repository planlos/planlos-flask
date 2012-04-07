# coding: utf-8

from tests import TestCase
from planlos.account_tools import (generate_activation_code,
                                   create_user,
                                   remove_user,
                                   create_group,
                                   remove_group,
                                   group_add,
                                   )
from planlos.documents import User_Exists_Exception, Group_Exists
from pymongo import Connection
from planlos.config import Testing

from nose.tools import raises
import re
import random

class Test_Account_Tools(TestCase):
    def setUp(self):
        t = Testing()
        self.connection = Connection()
        self.db = self.connection[t.MONGODB_DATABASE]

    def tearDown(self):
        self.db.users.remove( {'username': { '$regex' : 'testuser.*'} })
        self.db.groups.remove( {'name': { '$regex' : 'testuser.*'} })

    def get_random_username(self, prefix=u'testuser'):
        return prefix+unicode(int(random.random() * 10000))

    def test_generate_uuid(self):
        activation_code = generate_activation_code()
        regex = re.compile(
            '^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$'
            )
        self.assertTrue(re.match(regex, str(activation_code)).group(0),
                        str(activation_code))

    def test_create_user(self):
        testuser = self.get_random_username()
        create_user(testuser, u'randompass', u'planlos-test1@localhost')
        userdoc = self.db.users.find_one({'username': testuser})
        self.assertNotEqual(userdoc, None)
        groupdoc = self.db.groups.find_one({'name': testuser})
        self.assertNotEqual(groupdoc, None)
        print groupdoc
        doc = self.db.groupadmins.find_one({'group': groupdoc['_id']})
        self.assertIn(userdoc['_id'], doc['admins'])

    @raises(User_Exists_Exception)
    def test_create_existing_user(self):
        testuser = self.get_random_username()
        create_user(testuser, u'randompass', u'planlos-test1@localhost')
        # should fail:
        create_user(testuser, u'randompass', u'planlos-test1@localhost')

    def test_remove_user(self):
        testuser = self.get_random_username()
        create_user(testuser, u'randompass', u'planlos-test1@localhost')
        remove_user(testuser)
        userdoc = self.db.users.find_one({'username': testuser})
        self.assertEqual(userdoc, None)
        groupdoc = self.db.groups.find_one({'name': testuser})
        self.assertEqual(groupdoc, None)

    @raises(LookupError)
    def test_remove_nonexistent_user(self):
        testuser = self.get_random_username()
        remove_user(testuser)

    def test_create_group(self):
        testgroup = self.get_random_username()
        create_group(testgroup)
        groupdoc = self.db.groups.find_one({'name': testgroup})
        self.assertNotEqual(groupdoc, None)

    @raises(Group_Exists)
    def test_create_existing_group(self):
        testgroup = self.get_random_username()
        create_group(testgroup)
        create_group(testgroup)

    def test_add_user_to_group(self):
        testuser = self.get_random_username()
        create_user(testuser)
        testgroup = self.get_random_username()
        create_group(testgroup)
        group_add(testgroup, testuser)
        groupdoc = self.db.groups.find_one({'name': testgroup})
        userdoc = self.db.users.find_one({'username': testuser, 'groups': groupdoc['_id']})
        self.assertNotEqual(userdoc, None)

    def test_remove_group(self):
        testgroup = self.get_random_username()
        create_group(testgroup)
        remove_group(testgroup)
        groupdoc = self.db.groups.find_one({'name': testgroup})
        self.assertEqual(groupdoc, None)

    def test_remove_group_check_users(self):
        # setup
        testuser = self.get_random_username()
        create_user(testuser)
        testgroup = self.get_random_username()
        create_group(testgroup)
        group_add(testgroup, testuser)
        groupid = self.db.groups.find_one({'name': testgroup})['_id']
        # action
        remove_group(testgroup)
        # tests
        groupdoc = self.db.groups.find_one({'name': testgroup})
        self.assertEqual(groupdoc, None)
        userdoc = self.db.users.find({'groups': groupid})
        self.assertEqual(usersdoc, None)


    @raises(LookupError)
    def test_remove_non_existent_group(self):
        testgroup = self.get_random_username()
        remove_group(testgroup)



    def test_add_user_to_group(self):
        pass
        #testgroup = self.get_random_username()
        #create_group(testgroup)
        
