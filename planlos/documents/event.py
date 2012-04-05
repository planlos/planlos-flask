# coding: utf-8

from . import Document_with_Permissions
from user import User
from datetime import datetime
from planlos.extensions import db
from dateutil.parser import parse as date_parser
import config


class Event(Document_with_Permissions):
    __collection__ = 'events'
    structure = {
        'author': User,
        'title': unicode,
        'eventdate': datetime,
        'eventdate_end': datetime,
        'short_desc': unicode,
        'desc': unicode,
        'location': unicode,
        'gender': unicode,
        'url': unicode,
        'tags': [unicode],
        'rating': int,
        'is_published': bool,
        'created_at': datetime,
        'modified_at': datetime,
        }

    default_values = {
        'eventdate': datetime.now(),
        'rating': 0,
        'is_published': False,
        'created_at': datetime.now(),
        'modified_at': datetime.now(),
        }
    required = ['author', 'title', 'eventdate', 'location', 'is_published']

    def save_from_form(self, form, author_id):
        self.author = author_id
        # directly usable values
        self.title = form.title.data
        self.short_desc = form.short_desc.data
        self.desc = form.desc.data
        self.location = form.location.data
        self.url = form.url.data
        # fields with special handling
        self.gender = config.GENDER_CHOICES[form.gender.data]
        # tags =
        form_date = date_parser(form.eventdate_date.data).date()
        form_time = date_parser(form.eventdate_time.data).time()
        self.eventdate = datetime.combine(form_date, form_time)
        if form.eventdate2_date and form.eventdate2_time:
            form_date = date_parser(form.eventdate2_date.data).date()
            form_time = date_parser(form.eventdate2_time.data).time()
            self.eventdate_end = datetime.combine(form_date, form_time)
        self.tags = form.tags.data
        self.save()
        return self._id

    def get_author(self):
        return db.User.get(self.author)

    # Override permission
    def owner(self):
        return self.get_author()

    # Override permission
    def friends(self):
        try:
            return self.author.friends()
        except:
            return []

    @classmethod
    def create(cls, data):
        event = db.Event()
        for key, value in data.iteritems():
            event.__setattr__(key, value)
        event.save()
        return event

db.register([Event])
