# coding: utf-8

from tests import TestCase
from planlos.extensions import db
from flaskext.wtf import (Form, fields, widgets, HiddenField,
                          TextField, TextAreaField,
                          ListWidget, DateTimeField,
                          FormField, HiddenInput,
                          TextInput, FieldList,
                          required, BooleanField,
                          PasswordField, SubmitField,
                          Email, Required, ValidationError,
                          SelectField, URL, FloatField,
                          Optional, EqualTo)
from flaskext.mongokit import Document as MongoKit_Document
from planlos.fields import DateInputField, TimeInputField
from planlos.forms import Hidden_DateTimeField
from datetime import datetime


class SimpleEvent(MongoKit_Document):
    __collection__ = 'formtests'
    structure = {
        'date': datetime,
        'title': unicode,
        }
    use_dot_notation = True
    required = ['date', 'title']


class SimpleEventForm(Form):
    date_date = DateInputField("date")
    date_time = TimeInputField("time")
    date = Hidden_DateTimeField("hide")
    title = TextField("title")
    submit = SubmitField("save")

    def populate_obj(self, obj):
        combined = datetime.combine(self._fields['date_date'].data,
                                    self._fields['date_time'].data)
        self._fields['date'].data = combined.replace(microsecond=0)
        del self.date_date
        del self.date_time
        super(SimpleEventForm, self).populate_obj(obj)


class Test_Forms(TestCase):
    def setUp(self):
        db.register([SimpleEvent])
        db.formtests.drop()

    def test_save_to_db(self):
        sf = SimpleEventForm(None, None, date_date=datetime.now().date(),
                              date_time=datetime.now().time(),
                              title=u'Title')
        combined = datetime.combine(sf.date_date.data,
                                    sf.date_time.data).replace(microsecond=0)
        self.assertEqual(sf.validate(), True)
        e = db.formtests.SimpleEvent()
        sf.populate_obj(e)
        e.save()
        print combined
        print e.date
        e = db.SimpleEvent.find_one({'title': u'Title'})
        self.assertEqual(e.title, sf.title.data)
        self.assertEqual(e.date, combined)
