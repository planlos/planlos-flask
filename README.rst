Planlos App using flask
=======================

Rewrite of the current django-based planlos-app with Flask+MongoDB.


Dependencies
------------
* Flask
* Flaskext: Login, Mail, MongoKit, Script, Testing, WTF, (Sijax)
* mongokit
* pymongo
* nose + coverage.py
* python-dateutil
* running MongoDB


Development
-----------

For your convenience use virtualenv+pip, then

Run the development server::
     python manage.py runserver

Run the tests + coverage::
     python manage.py test


There are some management commands to fill your database with events from the current planlos. Or to add users, etc.
see ``manage.py``.
