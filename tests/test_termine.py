# coding: utf-8

from tests import TestCase
from datetime import datetime, date, time
from planlos.documents import Event
from planlos.extensions import db
from flask import current_app as app
from BeautifulSoup import BeautifulSoup
import random


class Test_Termine(TestCase):
    def setUp(self):
        db.events.drop()

    def create_termin_data(self):
        data = {
            'title': u'TestTitle' + unicode(int(random.random() * 10000)),
            'short_desc': u'TestShortDesc',
            'desc': u'TestDesc',
            'location': u'TestLocation',
            'url': u'http://test.de',
            'gender': 1,
            'eventdate_date': datetime.now().date(),
            'eventdate_time': datetime.now().time(),
            'tags': u'Konzert,Test,Cool'
            }
        return data

    def test_termine_index(self):
        response = self.client.get("/events/")
        self.assert_200(response)

    def test_unit_termin(self):
        data = self.create_termin_data()
        data['tags'] = list(set(data['tags'].split(',')))
        data['gender'] = app.config['GENDER_CHOICES'][data['gender']]

        e = Event.create(data)
        print "create_event: ", e._id
        e1 = db.Event.get_or_404(e._id)
        #print "Compare:"
        #print "AAA:"
        #for i in [x for x in e.iteritems()]:
        #    print i
        #print "BBB:"
        #for i in [x for x in e1.iteritems()]:
        #    print i
        self.assertEquals(e, e1)

    def test_add_termin(self):
        self.login_as_user()
        data = self.create_termin_data()
        response = self.client.post("/events/add", data=data)
        e = db.Event.find({'title': data['title']})
        self.assertEqual(e.count(), 1)
        e = e[0]
        print "DEBUG.: ", e.tags
        assert('Konzert' in e.tags)
        assert('Test' in e.tags)
        assert('Cool' in e.tags)
        self.assert_redirects(response, "/events/%s" % e._id)
        print e._id
        response = self.client.get("/events/%s" % e._id)
        self.assert200(response)
        self.assertContext('event', e)

    def test_dateinput_css_class(self):
        self.login_as_user()
        response = self.client.get("/events/add")
        b = BeautifulSoup(response.data)
        dateinput = b.body.findAll(id='eventdate_date')[0]
        assert dateinput['class'] == 'eventdate_picker'
        dateinput = b.body.findAll(id='eventdate_time')[0]
        assert dateinput['class'] == 'eventtime_picker'

    def test_termine_edit(self):
        self.login_as_user()
        data = self.create_termin_data()
        response = self.client.post("/events/add", data=data)

    def test_add_termin2(self):
        self.login_as_user()
        data = {
            'title': 'TestTitle2',
            'short_desc': 'TestShortDesc2',
            'desc': 'TestDesc2',
            'location': 'TestLocation2',
            'url': 'http://test2.de',
            'gender': 1,
            'eventdate_date': datetime.now().date(),
            'eventdate_time': datetime.now().time(),
            'eventdate_end_date': datetime.now().date(),
            'eventdate_end_time': datetime.now().time(),
            'tags': 'ZweiZeiten,Konzert,Test,Cool'
            }
        response = self.client.post("/events/add", data=data) #, follow_redirects=True
        #self.assert_200(response)
        e = db.Event.find({'title': data['title']})
        assert(e.count() == 1)
        e = e[0]
        # einmal eine Methode, die ALLE data Fields prueft
        assert('ZweiZeiten' in e.tags)
        assert('Konzert' in e.tags)
        assert('Test' in e.tags)
        assert('Cool' in e.tags)
        assert(e.eventdate.utctimetuple() == datetime.combine(data['eventdate_date'],
                                                              data['eventdate_time']).utctimetuple())
        assert(e.eventdate_end.utctimetuple() == datetime.combine(data['eventdate_end_date'],
                                                                  data['eventdate_end_time']).utctimetuple())
        self.assert_redirects(response, "/events/%s" % e._id)
        response = self.client.get("/events/%s" % e._id)
        #self.assertContext( 'event', e)

