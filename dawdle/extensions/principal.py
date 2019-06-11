"""
Flask-Principal extension.
"""

from flask_login import current_user
from flask_principal import identity_loaded, Principal, UserNeed

principal = Principal()

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    """
    Adds additional information to identity instances such as roles.
    """

    identity.user = current_user

    identity.provides.add(UserNeed(current_user.get_id()))
