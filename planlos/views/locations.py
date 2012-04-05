# coding: utf-8

from flask import Blueprint, g, render_template, redirect, url_for, flash, request, session
from flask import current_app as app
from planlos.forms import Location_Form
from planlos.extensions import db
from planlos.documents import Location
from flaskext.login import login_required

locations = Blueprint('locations', __name__)

@locations.route('/')
def index():
    locations = db.Location.find({})
    return render_template('locations/index.html', locations = locations)


@locations.route('/add', methods = ['GET', 'POST'])
def add():
    form = Location_Form()

    if form.validate_on_submit():
        location = Location(name = form.name.data,
                            contact = form.contact.data,
                            desc = form.desc.data,
                            address = form.desc.data,
                            loc = (form.long.data, form.lat.data)
                           )
        location.save()
        loc_id = location.mongo_id
        return redirect( url_for('locations.show', loc_id = location.mongo_id))
    return render_template('locations/add.html', form = form)

@locations.route('/<ObjectId:loc_id>')
def show(loc_id):
    location = db.Location.get_or_404(loc_id)
    return render_template('locations/show.html', location = location)


@locations.route('/<ObjectId:loc_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(loc_id):
    location = db.Location.get_or_404(loc_id)
    form = Location_Form(request.form , obj=location)
    if form.validate_on_submit():
        form.populate_obj(location)
        location.save()
        return redirect( url_for('locations.show', loc_id = location._id))
    return render_template('locations/edit.html', form = form)

@locations.route('/<ObjectId:loc_id>/delete')
@login_required
#@moderator.require()
def delete(loc_id):
    location = db.Location.get_or_404(loc_id)
    location.remove()
    return redirect( url_for('locations.index'))



