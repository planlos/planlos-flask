0#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, g
from planlos.views.calendar import calendar
from planlos.views.accounts import accounts
from planlos.views.locations import locations
from planlos.views.groups import groups
from planlos.views.base import base
from planlos.views.admin import admin
from planlos.webservices import webservice
from planlos.extensions import mail, db, login_manager
from planlos.documents import User, Group
import flask_sijax
from flaskext.login import user_logged_in
import datetime

from template_widgets import widget

__all__ = ["create_app"]


# login signaal
def set_login_stamp(sender, user, **extra):
    user.last_login = datetime.datetime.now()


def create_app(config='planlos.config.Config'):
    app = Flask('planlos')
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    flask_sijax.Sijax(app)
    # Flask Login
    login_manager.setup_app(app)
    app.register_blueprint(base, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(calendar, url_prefix='/events')
    app.register_blueprint(accounts, url_prefix='/users')
    app.register_blueprint(locations, url_prefix='/locations')
    app.register_blueprint(webservice, url_prefix='/webservice')
    app.register_blueprint(groups, url_prefix='/groups')

    app.jinja_env.globals['widget'] = widget

    user_logged_in.connect(set_login_stamp, app)
    return app


@login_manager.user_loader
def load_user(userid):
    return db.User.get_by_name(userid)
