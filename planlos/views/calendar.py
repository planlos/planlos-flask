# coding: utf-8
from flask import (Blueprint, g, render_template,
                   request, redirect, url_for, abort)
from flask import current_app as app
from flaskext.login import login_required, current_user
from planlos.documents import User, Event
from planlos.forms import Event_Form
from planlos.extensions import db
#from planlos.fields import GenderSelectField
from datetime import datetime, timedelta

from planlos.permissions import Grant, UserPermission

calendar = Blueprint('calendar', __name__)


@calendar.route('/')
def index():
    events = db.Event.find({})
    return render_template("calendar/index.html", events=events)


@calendar.route('/<ObjectId:event_id>')
def show(event_id):
    event = db.Event.get_or_404(event_id)
    return render_template("calendar/show.html", event=event)


@calendar.route('/<ObjectId:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    event = db.Event.get_or_404(event_id)
    with Grant(event, current_user, 'update'):
        form = Event_Form(request.form, obj=event)
        if form.validate_on_submit():
            form.populate_obj(event)
            event.save()
            return redirect(url_for('calendar.show', event_id=event_id))
        return render_template("calendar/edit.html", form=form)


@calendar.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = Event_Form()
    if request.method == 'POST':
        form.author = current_user._id
        if form.validate_on_submit():
            event = db.Event()
            form.populate_obj(event)
            event.save()
            return redirect(url_for('calendar.show', event_id=event._id))
    return render_template("calendar/add.html", form=form)


@calendar.route('/_query/events_by_user/')
@login_required
def query():
    user = db.User.get_by_name(request.args.get('u'))
    print "DEBUG ", user
    if user != current_user:
        abort(403)
    userevents = db.Event.find({'author': user._id})
    return render_template("calendar/_query_events_by_user.html",
                           userevents=userevents)


@calendar.route('/<year>/<month>/<day>/', methods=['GET'])
def by_date(year, month, day):
    today = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
    tomorrow = today + timedelta(days=1)
    events = db.Event.find({'eventdate': {'$lt': tomorrow, '$gt': today}})
    return render_template("calendar/day.html", events=events)
