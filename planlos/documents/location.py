# coding: utf-8
from . import Document
from planlos.extensions import db

class Location(Document):
    __collection__ = 'locations'
    structure = {
        'name': unicode,
        # alternativer name?
        # sielwallhaus, swh, etc
        'contact': unicode,
        'desc': unicode,
        'address': unicode,
        'loc': [float, float],
        'url': unicode,
        }
    required = ['name', 'contact', 'desc', 'address']

db.register([Location])
