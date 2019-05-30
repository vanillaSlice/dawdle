"""
Flask-Login extension.
"""

from flask_login import LoginManager

from dawdle.models.user import User
from dawdle.utils import to_ObjectId

login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """
    This callback is used to reload the user object from the user
    ID stored in the session.
    """

    return User.objects(auth_id=to_ObjectId(user_id)).first()
