# coding: utf-8
from flask import Blueprint, g, render_template, redirect, url_for
from flask import current_app as app
from flask import flash, request, session

base = Blueprint('base', __name__)

@base.route('/')
def index():
    return render_template('index.html')

