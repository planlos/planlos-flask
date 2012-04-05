# coding: utf-8

from flask import Blueprint, g, render_template, redirect, url_for
from flask import current_app as app
from flask import flash, request, session
from planlos.extensions import db
from flaskext.login import login_required
from planlos.documents import Profile, User, Event, Group

from flaskext.wtf import (Form, HiddenField,
                          TextField, TextAreaField,
                          required, BooleanField,
                          PasswordField, SubmitField,
                          Email, Required, ValidationError,
                          DateTimeField, FormField,
                          SelectField, URL, FloatField,
                          Optional, EqualTo)

import datetime

admin = Blueprint('admin', __name__)



fmap = {
    unicode: TextField,
    float: FloatField,
    bool: BooleanField,
    datetime.datetime: DateTimeField
}

class Role_Form(Form):
    authenticated = BooleanField(u'authenticated', default = False)
    moderator = BooleanField(u'Moderator', default = False)
    admin = BooleanField(u'Admin', default = False)

    def populate(self, roles):
        if u'authenticated' in roles:
            self.authenticated.data = True
        if u'moderator' in roles:
            self.moderator.data = True
        if u'admin' in roles:
            self.admin.data = True

class Profile_Form(Form):
    email = TextField(u'Email', validators = [Email("not a valid email adress")])

    def populate(self, profile):
        self.email.data = profile.email


class User_Management_Form(Form):
    username = TextField(u'Username')
    password = PasswordField(u'Passwort')
    displayname = TextField(u'displayname')
    signup_email = TextField(u'Signup Email')
    activation_key = TextField(u'Activation key')
    roles = FormField(Role_Form)
    profile  = FormField(Profile_Form)
    active = BooleanField(u'active')
    submit = SubmitField("Save")

    def populate(self, user):
        self.username.data = user.username
        self.password.data = user.password
        self.displayname.data = user.displayname
        self.signup_email.data = user.signup_email
        self.active.data = user.active
        self.activation_key.data = user.activation_key
        self.roles.populate(user.roles)
        self.profile.populate(user.profile)


class Admin_Form(Form):
    submit = SubmitField("Save")

    def populate(self, dbobj):
        for key,val in dbobj.structure.iteritems():
            try:
                self.__setattr__(key, val)
            except:
                print "could not set value for key", key

    @classmethod
    def dynform(self, dbobj):
        for key,val in dbobj.structure.iteritems():
            try:
                setattr(Admin_Form, key, fmap[val](key) )
            except:
                print "cannot display value", val

@admin.route('/people/<uid>', methods=["GET", "POST"])
def people(uid):
    user = db.User.find_one_or_404({'username': uid})
    form = User_Management_Form()
    form.populate(user)
    return render_template('admin/user.html', form=form, user=user)


@admin.route('/')
#@login_required
def index():
    c = {}
    # get some statistics
    event_count = db.events.count()
    c.update({'event_count': event_count})
    user_count = db.User.find({'active': True}).count()
    c.update({'active_user_count': user_count})
    return render_template('admin/index.html', **c)

