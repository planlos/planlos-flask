# coding: utf-8

from flask import Blueprint, render_template, request
from flask import current_app as app
from planlos.extensions import db
from planlos.documents import Location, Event
import simplejson as json
from datetime import datetime, timedelta
import re


webservice = Blueprint('webservice', __name__)


@webservice.route('/locations/', methods=['GET'])
def locations():
    search_term = request.args.get('term', '')
    search_term = re.escape(search_term)
    locations = db.Location.find({'name':
                                      {'$regex': search_term, '$options': 'i'}})
    ret = []
    for loc in locations:
        ret.append(loc.name)
    return json.dumps(ret)


@webservice.route('/tags/', methods=['GET'])
def tags():
    search_term = request.args.get('term', '')
    search_term = re.escape(search_term)
    tags = db.Event.find({'tags':
                              {'$regex': search_term, '$options': 'i'}}, {'tags': 1})
    taglist = []
    for tag in tags:
        taglist.extend(tag['tags'])
    ret = []
    for tag in taglist:
        if re.search(search_term, tag, re.IGNORECASE) != None:
            #print "Matched: ", tag
            ret.append(tag)
    return json.dumps(ret)


@webservice.route('/events/<year>/<month>/<day>')
def events_by_date(year, month, day):
    #if request.args.get('format', 'html')
    today = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
    tomorrow = today + timedelta(days=1)
    events = db.Event.find({'eventdate': {'$lt': tomorrow, '$gt': today}})
    return render_template('webservice/events_by_date.html', events=events)
