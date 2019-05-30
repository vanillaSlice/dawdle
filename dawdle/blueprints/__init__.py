"""
Exports Dawdle app blueprints.
"""

from dawdle.blueprints.auth import auth
from dawdle.blueprints.home import home
from dawdle.blueprints.user import user

blueprints = [auth, home, user]
