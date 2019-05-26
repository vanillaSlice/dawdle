"""
Exports Flask extensions used.
"""

from flask_assets import Environment
from flask_login import LoginManager
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect

from dawdle.assets import bundles
from dawdle.models.user import User
from dawdle.utils import to_ObjectId

#
# Flask-Assets
#

assets = Environment()
assets.register(bundles)

#
# Flask-WTF
#

csrf = CSRFProtect()

#
# Flask-Login
#

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """
    This callback is used to reload the user object from the user
    ID stored in the session.
    """

    return User.objects(auth_id=to_ObjectId(user_id)).first()

#
# Flask-Mail
#

mail = Mail()

#
# Flask-MongoEngine
#

mongoengine = MongoEngine()
