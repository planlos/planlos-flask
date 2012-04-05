# coding: utf-8

from . import Document
from flaskext.login import UserMixin
from planlos.passwordgen import Password_Generator
from flaskext.mail import Message
from planlos.extensions import mail, db
from validators import email_validator
from datetime import datetime
from group import Group

class User_Exists_Exception(Exception):
    pass


class User(Document, UserMixin):
    __collection__ = 'users'
    structure = {
        'username': unicode,
        'password': unicode,
        'displayname': unicode,
        'signup_email': unicode,
        'date_joined': datetime,
        'last_login': datetime,
        'profile': {'email': unicode},
        'activation_key': unicode,
        'active': bool,
        'roles': [unicode],
        'groups': [Group]
        }

    use_autorefs = True

    required = ['username', 'password', 'signup_email', 'roles']
    default_values = {
        'active': False,
        'displayname': u'',
        'date_joined': datetime.now(),
        'last_login': datetime.now(),
        'roles': [u'authenticated'],
        }

    def check_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def activate_by_code(self, code):
        if self.activation_key == code:
            self.active = True
            self.save()
            return True
        else:
            return False

    def has_role(self, role):
        return role in self.roles

    def reset_password(self):
        p = Password_Generator()
        passwd = p.gen()
        # check email
        email = self.signup_email
        if self.profile.email in ['', None]:
            email = self.profile.email
        # mailout passwort
        reset_msg = Message("Hello",
                            sender="accounts@planlosbremen.de",
                            recipients=[email])
        reset_msg.body = """Your new Passwort is: %s""" % (passwd)
        mail.send(reset_msg)
        self.password = passwd
        return passwd

    @classmethod
    def authenticate(cls, username, password):
        user = cls.get_by_name(username)
        if user and user.active:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def create(cls, **kwargs):
        if 'username' in kwargs and User.exists(kwargs['username']):
            raise User_Exists_Exception()
        user = db.User()
        for key, value in kwargs.iteritems():
            print "create: ", key, value
            user.__setattr__(key, value)
        user.save()
        return user

    @classmethod
    def exists(cls, username):
        user = db.User.find_one({'username': username})
        if user is not None:
            return True
        else:
            return False

    @classmethod
    def get_by_name(cls, username):
        return db.User.find_one_or_404({'username': username})

    def get_id(self):
        return self.username


    def __repr__(self):
        if len(self.displayname):
            return self.displayname
        else:
            email = self.profile.email
            if not email:
                email = self.signup_email
            return self.username + " (%s)" % email

    def events(self):
        return db.Event.find({'author': self})


db.register([User])


