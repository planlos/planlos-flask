# coding: utf-8

from . import Document, DocumentExistsException
from . import db


class Group_Exists(DocumentExistsException):
    pass

class Group (Document):
    __collection__ = 'groups'
    structure = {
        'name': unicode,
        'desc': unicode,
        'what_tags': [unicode],
        'where_tags': [unicode],
        'public': bool,
        'homepage_url': unicode,
        #'planlospage': Homepage,
        }

    required = ['name']

    @classmethod
    def create(cls, name, desc='', homepage_url='', members=[]):
        if not cls.exists(name):
            g = db.Group()
            g.name = name
            g.desc = desc
            g.homepage_url = homepage_url
            g.members = members
            g.save()
            return g
        raise DocumentExistsException()

    @classmethod
    def exists(cls, groupname):
        group = cls.get_by_name(groupname)
        if group:
            return True
        else:
            return False

    @classmethod
    def get_by_name(cls, groupname):
        group = db.Group.find_one({'name': groupname})
        return group


db.register([Group])
