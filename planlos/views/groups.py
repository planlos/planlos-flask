# coding: utf-8

from flask import Blueprint, g, render_template, redirect, url_for
from flask import current_app as app
from flask import flash, request, session
from planlos.forms import Group_Form
from planlos.documents import Profile, User, Group
from flaskext.login import login_required
import uuid
from planlos.extensions import mail

groups = Blueprint('groups', __name__)

