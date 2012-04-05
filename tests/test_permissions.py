# coding: utf-8

from tests import TestCase
from planlos.permissions import Grant, PermissionDenied


class Test_Permissions(TestCase):
    class Role_Provider(object):
        def __init__(self):
            self.roles = ['authenticated']

    class Perm_Object(object):
        def __init__(self):
            self.permissions = {
                'show': ["authenticated", "friend"],
                'update': ["moderator"],
                'copy': ["authenticated", "friend"],
                'delete': ["friend"],
                'notify': ["friend"]
                }
            self.friends = []
            self.owner = None

            def _need_owner(self, role_provider):
                print role_provider
                if self.owner() != role_provider:
                    raise PermissionDenied()

            def _need_friend(self, role_provider):
                print role_provider
                if role_provider not in self.owner().friends():
                    raise PermissionDenied()

            def _need_group(self, role_provider):
                print role_provider
                if role_provider not in self.owner().friends():
                    raise PermissionDenied()

            def owner(self):
                return self.owner

            def friend(self):
                return self.friends

    def setUp(self):
        # users
        self.anon_user = Test_Permissions.Role_Provider()
        self.anon_user.roles = []

        self.user1 = Test_Permissions.Role_Provider()
        self.user1.roles = ["authenticated"]

        self.user2 = Test_Permissions.Role_Provider()
        self.user2.roles = ["authenticated"]

        self.user3 = Test_Permissions.Role_Provider()
        self.user3.roles = ["authenticated"]

        self.mod = Test_Permissions.Role_Provider()
        self.mod.roles = ["moderator"]

        self.admin = Test_Permissions.Role_Provider()
        self.admin.roles = ["admin"]

        # objects
        self.obj1 = Test_Permissions.Perm_Object()
        self.obj1.owner = self.user1
        self.obj1.friends = [self.user2]

    def test_owner_update(self):
        with Grant(self.obj1, self.user1, 'update'):
            pass

    def test_authenticated_show(self):
        with Grant(self.obj1, self.user1, 'show'):
            pass

    def test_friend_notify(self):
        with Grant(self.obj1, self.user3, 'notify'):
            pass

    def test_deny_nonowner_update(self):
        g = Grant(self.obj1, self.user1, 'update')
        self.assertRaises(PermissionDenied, g.__enter__())

    def test_deny_authenticated_show(self):
        g = Grant(self.obj1, self.anon_user, 'show')
        self.assertRaises(PermissionDenied, g.__enter__())

    def test_deny_nonfriend_notify(self):
        g = Grant(self.obj1, self.user2, 'notify')
        self.assertRaises(PermissionDenied, g.__enter__())

