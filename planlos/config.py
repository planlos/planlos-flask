# coding: utf-8
# internal pre-defined variables of flask
import os

from documents.config import GENDER_CHOICES

class Config(object):
    DEBUG = True
    TESTING = False
    # PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = "nnuunnneenrrenereslakfjewrlkjasflflkjsdwerowqierh50175c98ß43czmgr9u,hd497t"
    SESSION_COOKIE_NAME = "c_planlos"
    # PERMANENT_SESSION_LIFETIME = # datetime.timedelta
    #USE_X_SENDFILE = True
    LOGGER_NAME = 'planlos-app'
    #SERVER_NAME = # for subdomains
    #MAX_CONTENT_LENGTH = # in bytes

    SIJAX_STATIC_PATH = os.path.join('.', os.path.dirname(__file__), 'static/sijax/')
    SIJAX_JSON_URI = '/static/sijax/json2.js'

    ## Application Variables
    GENDER_CHOICES = GENDER_CHOICES

class Development(Config):
    DEBUG = True
    MONGODB_DATABASE = 'planlos_flask_dev'


class Testing(Config):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = False
    MONGODB_DATABASE = 'planlos_flask_test'
