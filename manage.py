# coding: utf-8
import sys
import os

from datetime import datetime
from dateutil.parser import parse as date_parser
import simplejson


def test():
    import nose
    from nose import plugins
    from nose.plugins import cover
    import shutil
    try:
        shutil.rmtree("cover")
    except:
        pass
    args = ["--with-coverage",
            "--cover-erase",
            "--cover-package=planlos",
            "--cover-inclusive",
            "--cover-html",
            ]
    sys.argv += args
    sys.argv += ["tests"]
    nose.main(addplugins=[cover.Coverage()])


def setup():
    from planlos.documents import Event, User, Profile, Location

    def _make_context():
        return dict(Event=Event, User=User, Profile=Profile, Location=Location)

    manager.add_command("shell", Shell(make_context=_make_context))
    manager.add_command("runserver", Server())

    @manager.command
    def adduser(user, password, email, moderator=False):
        # create normal user
        a = unicode(uuid.uuid1())
        u = User.create(username=unicode(user),
                        password=unicode(password),
                        signup_email=unicode(email),
                        activation_key=a,
                        )
        u.active = True
        if moderator:
            u.roles.append(u"moderator")
        u.save()

    @manager.command
    def suckdry_planlos():
        import urllib
        f = urllib.urlopen("http://planlosbremen.de/termine/service/monat")
        #https://planlosbremen.de/termine/service/location/5
        #jsondata = f.read()
        data = simplejson.load(f)
        u = db.User.find_one()
        for i in data:
            loc_id = i['fields']['location']
            url = urllib.urlopen("http://planlosbremen.de/termine/service/location/%s" % loc_id)
            loc = simplejson.load(url)
            location = loc_name = loc[0]['fields']['name']
            e = db.Event()
            f = i['fields']
            e.title = unicode(f['title'])
            e.author = u
            form_date = date_parser(f['datum']).date()
            form_time = date_parser(f['time']).time()
            e.eventdate = datetime.combine(form_date, form_time)
            e.short_desc = unicode(f['short_desc'])
            e.desc = unicode(f['desc'])
            e.url = unicode(f['exturl'])
            e.tags = [unicode(f['type'])]
            e.is_published = f['is_pub']
            e.save()

    @manager.command
    def load_location(jsonfile):
        f = open('locations4.json')
        json = simplejson.load(f)
        for loc in json:
            loc = loc['fields']
            location = db.Location()
            #'name', 'selfportrait', 'url', 'image', 'address', 'streetmap'
            location.name = unicode(loc['name'])
            location.desc = unicode(loc['selfportrait'])
            location.url = unicode(loc['url'])
            location.address = unicode(loc['address'])
            location.contact = unicode(loc['url'])
            location.save()


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    else:
        from flask import app
        from flaskext.script import Shell, Server, Manager

        from planlos import create_app
        from planlos.config import Development

        app = create_app(Development())
        manager = Manager(app)
        manager.add_option('-c', '--config', dest='config', required=False)
        setup(manager)
        manager.run()
