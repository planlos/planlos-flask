# coding: utf-8

from . import Document
from validators import email_validator
from planlos.extensions import db

class Profile(Document):
    __collection__ = 'profile'

    structure = {
        'email': unicode,
        }

    validators = {
        'email': email_validator,
        }

db.register([Profile])
