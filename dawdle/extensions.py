"""
Exports Flask extensions used.
"""

from flask_assets import Environment
from flask_login import LoginManager
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect

assets = Environment()

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

mail = Mail()

mongoengine = MongoEngine()
