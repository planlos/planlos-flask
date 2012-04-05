# coding: utf-8
from . import Document
from planlos.extensions import db

class Homepage(Document):
    structure = {
        'title': unicode,
        'content': unicode,
        }
    required = ['title', 'content']

db.register([Homepage])
