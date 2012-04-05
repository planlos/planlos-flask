# coding: utf-8

from tests import TestCase
from datetime import datetime, date, time
from planlos.documents import Group


#class Test_Group(TestCase):
#    def test_group_index(self):
#        self.login_as_moderator()
#        response = self.client.get("/groups/")
#        self.assert_200(response)###

#    def test_create_group(self):
#        self.login_as_moderator()
#        data = { 'name': 'Planlos-Crew',
#                 'desc': 'Beschreibung',
#                 'homepage_url': 'http://planlosbremen.de'
#            }
#        response = self.client.post("/groups/create", data=data, foll#ow_redirects=True)
#        self.assert_200(response)
#        g = Group.query.filter({'name': data['name']}).one()
