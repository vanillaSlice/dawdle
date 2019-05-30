"""
Exports extensions used by the Dawdle app.
"""

from dawdle.extensions.assets import assets
from dawdle.extensions.login import login_manager
from dawdle.extensions.mail import mail
from dawdle.extensions.mongoengine import mongoengine
from dawdle.extensions.wtf import csrf

extensions = [assets, csrf, login_manager, mail, mongoengine]
