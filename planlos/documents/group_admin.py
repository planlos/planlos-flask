# coding: utf-8

from . import Document
from planlos.extensions import db

from group import Group
from user import User
import bson

class Group_Admin(Document):
    __collection__ = 'groupadmins'
    structure = {
        'group' : bson.objectid.ObjectId,
        'admins': [bson.objectid.ObjectId]
        }

    use_autorefs = True
    required = ['group', 'admins']


db.register([Group_Admin])
