# coding: utf-8
from flaskext.mail import Mail
from flaskext.mongokit import MongoKit
from flaskext.login import LoginManager

login_manager = LoginManager()
db = MongoKit()
mail = Mail()
