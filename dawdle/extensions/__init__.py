"""
Exports extensions used by the Dawdle app.
"""

from dawdle.extensions.assets import assets
from dawdle.extensions.login import login_manager
from dawdle.extensions.mail import mail
from dawdle.extensions.mongoengine import mongoengine

extensions = [assets, login_manager, mail, mongoengine]
