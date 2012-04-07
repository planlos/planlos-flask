# coding: utf-8

from datetime import datetime
from flaskext.mongokit import Document as MongoKit_Document
from planlos.permissions import PermissionDenied
from flaskext.login import UserMixin
from planlos.extensions import db
from types import NoneType

class DocumentExistsException(Exception):
    pass


class Document(MongoKit_Document):
    structure = {
        'created_at': datetime,
        'modified_at': datetime
        }

    default_values = {
        'created_at': datetime.now(),
        'modified_at': datetime.now(),
        }

    use_dot_notation = True

    def url_for(self):
        return "/" + "/".join(
            [str(self.__collection__), str(self._id)])

    def __eq__(self, other):
        if type(other) is NoneType:
            return False
        return self._id == other._id


class Document_with_Permissions(Document):
    structure = {
        'permissions': dict,
        }

    default_values = {
        'permissions': {
            'show': ['all'],
            'add': ['authenticated', 'moderator'],
            'delete': ['moderator'],
            'copy': ['moderator', 'friend', 'group'],
            'update': ['moderator', 'friend', 'group'],
            'notify': ['friend', 'group'],
            }
        }

    def _need_owner(self, role_provider):
        if self.owner() != role_provider:
            return False
        else:
            return True

    def _need_friend(self, role_provider):
        if role_provider not in self.owner().friends():
            return False
        else:
            return True

    def _need_group(self, role_provider):
        if role_provider not in self.owner().friends():
            return False
        else:
            return True

    def owner(self):
        return None

    def friend(self):
        return [None]

from user import User, User_Exists_Exception
from group import Group, Group_Exists
from group_admin import Group_Admin
from profile import Profile
from event import Event
from location import Location
