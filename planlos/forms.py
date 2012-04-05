# coding: utf-8
from flask import current_app as app
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
from documents import User, Group, Event, Profile
import re
import uuid
from planlos.fields import DateInputField, TimeInputField
from planlos.extensions import db
from datetime import datetime


class Login_Form(Form):
    next = HiddenField()
    remember = BooleanField("Remember me")
    username = TextField("Username",
                         validators=[ required(message="You must provide a username")])
    password = PasswordField("Password")
    submit = SubmitField("Login")


class Signup_Form(Form):
    next = HiddenField()
    username = TextField("Username",
                         validators=[required(message="You must provide a username")])
    password = PasswordField("Password",
                             validators=[Required()])
    password2 = PasswordField("Repeat Password",
                              validators=[EqualTo('password',
                                                  message='Passwords do not match')]
                              )
    email = TextField("E-Mail",
                      validators=[Required(),
                                  #Email("not a valid email adress")
                                  ])
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        username = field.data
        if not re.match('[a-zA-Z][0-9a-zA-Z\.+-]+', username):
            raise ValidationError('Username has invalid Characters')
        if User.exists(username) or Group.exists(username):
            raise ValidationError('Username is already taken')


    def get_activation_code(self):
        return self.activation_code

    def save_user(self):
        u = db.User()
        u.username = self.username.data
        u.password = self.password.data
        u.signup_email = self.email.data
        u.activation_key = self.generate_activation_code()
        u.save()
        return u




## Date validator
from dateutil.parser import parse as date_parser
def validate_date(form, field):
    try:
        d = date_parser(field.data)
    except:
        raise ValidationError("Cannot parse Date")


#    def as_html(self):
#        htmlstring = ''
#        display_tags = []
#        span = """<p><span>%s</span><a class="removetag" value="%s" href="">(-)</a></p>"""
#        if self.tags.data:
#            for tag in self.tags.data.split(','):
#                display_tags.append(tag)
#        s = set(display_tags)
#        for tag in list(s):
#            htmlstring += span %(tag, tag)
#        return htmlstring


class TagListField(fields.Field):
    widget = HiddenInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

    def __call__(self, **kwargs):
        htmlstring = """<input type="text" name="%s" value="%s" %s> """ % (self.name, self._value(), widgets.html_params(**kwargs) )
        #htmlstring += '<div id="taglist">'
        #for value in self.data:
        #    htmlstring += """<span class='tag' value="%s">%s</span><span class="removetag" onclick="remove_tag2('%s');">&otimes;</span>""" % (value, value,value)
        #htmlstring += "</div>"
        return widgets.HTMLString(htmlstring)


class Hidden_DateTimeField(fields.Field):
    widget = HiddenInput()

    def _value(self):
        if self.data:
            return unicode(str(self.data))
        else:
            return u''

    def process_formdata(self, date):
        if date:
            self.data = date_parser(date[0])
        else:
            self.data = None


class GenderField(SelectField):
    def __init__(self, **kwargs):
        self.choices = [(id, name) for id,name in app.config['GENDER_CHOICES'].iteritems()]
        super(GenderField, self).__init__(**kwargs)

    def process_formdata(self, gender):
        if gender:
            self.data = int(app.config['GENDER_CHOICES'][gender])
        else:
            self.data = None


class Event_Form(Form):
    author = HiddenField()
    title = TextField("Title", validators=[Required()])
    eventdate_date = DateInputField("Date",
                                    validators=[Required()])
    eventdate_time = TimeInputField("Time",
                                    validators=[Required()])
    eventdate_end_date = DateInputField("Date")
    eventdate_end_time = TimeInputField("Time")
    eventdate = Hidden_DateTimeField("")
    eventdate_end = Hidden_DateTimeField("")
    short_desc = TextField("Short description")
    desc = TextAreaField("Description")
    location = TextField("Location")
    gender = SelectField("Gender", coerce=int)  # ? (needs choices in view)
    url = TextField("Event URL/More Info", validators=[Optional(), URL(require_tld=False)])
    tags = TagListField("Tags")
    submit = SubmitField("Save")

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(Event_Form, self).__init__(formdata, obj, prefix, **kwargs)
        self.gender.choices = [ (id, name) for id,name in app.config['GENDER_CHOICES'].iteritems() ]


    def populate_obj(self, obj):
        combined = datetime.combine(self._fields['eventdate_date'].data,
                                    self._fields['eventdate_time'].data)
        self._fields['eventdate'].data = combined
        if self._fields['eventdate_end_date'].data and self._fields['eventdate_end_time'].data:
            combined = datetime.combine(self._fields['eventdate_end_date'].data,
                                        self._fields['eventdate_end_time'].data)
            self._fields['eventdate_end'].data = combined
        del self.eventdate_date
        del self.eventdate_time
        del self.eventdate_end_date
        del self.eventdate_end_time
        self.gender.data = unicode(app.config['GENDER_CHOICES'][self.gender.data])
        super(Event_Form, self).populate_obj(obj)

#    def create_from(self, event):
#        self.gender.choices = [ (id, name) for id,name in gender_choices.iteritems() ]
#        self.tags.data = event.tags
#        if event.eventdate is not None:
#            self.eventdate_date.data = event.eventdate.date()
#            self.eventdate_time.data = event.eventdate.time()
#        if event.eventdate_end is not None:
#            self.eventdate2_date.data = event.eventdate_end.date()
#            self.eventdate2_time.data = event.eventdate_end.time()

class Location_Form(Form):
    name = TextField("Name", validators = [ Required()] )
    contact = TextField("Kontakt", validators = [ Required()] )
    desc = TextField("Beschreibung", validators = [ Required()] )
    address = TextField("Adresse", validators = [ Required()] )
    loc = FieldList( FloatField("", validators = [ Optional() ], default = 0.0), max_entries = 2, min_entries = 2)
    submit = SubmitField("Save")

class Group_Form(Form):
    name = TextField("Name", validators = [ Required()] )
    desc = TextField("Beschreibung", validators = [ Required()] )
    homepage_url = TextField("Homepage URL", validators = [ Optional() ] )
    submit = SubmitField("Create")

