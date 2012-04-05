# coding: utf-8

from flask import current_app as app
from flaskext.wtf import TextField, TextInput
from dateutil.parser import parse as date_parser
import datetime
# Form Fields Special


class DateInputField(TextField):
    def __call__(self, **kwargs):
        kwargs['class'] = "eventdate_picker"
        kwargs['class_'] = "eventdate_picker"
        return super(DateInputField, self).__call__(**kwargs)

    def _value(self):
        if self.data:
            return unicode(str(self.data))
        else:
            return u''

    def process_formdata(self, date):
        if date:
            self.data = date_parser(date[0], default=datetime.datetime.now()).date()
        else:
            self.data = None

    def validate(self, form, extra_validators=()):
        return True


class TimeInputField(TextField):
    def __call__(self, **kwargs):
        kwargs['class'] = "eventtime_picker"
        kwargs['class_'] = "eventtime_picker"
        return super(TimeInputField, self).__call__(**kwargs)

    def _value(self):
        if self.data:
            return unicode(str(self.data))
        else:
            return u''

    def process_formdata(self, date):
        if date:
            self.data = date_parser(date[0], default=datetime.datetime.now()).time()
        else:
            self.data = None

    def validate(self, form, extra_validators=()):
        return True
