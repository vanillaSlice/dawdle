"""
Exports Dawdle app blueprints.
"""

from dawdle.blueprints.auth import auth
from dawdle.blueprints.contact import contact
from dawdle.blueprints.home import home
from dawdle.blueprints.user import user

blueprints = [auth, contact, home, user]
