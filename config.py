"""
Contains default and test config properties. To add local instance
config properties create a file 'instance/config.py' or export the
properties as environment variables (note that environment variables
will take precedence).
"""

class Default:
    """
    Default config properties.
    """

    DEBUG = False
    ENV = 'production'
    SECRET_KEY = 'default secret key'
    SERVER_NAME = '127.0.0.1:5000'
    SESSION_COOKIE_DOMAIN = '127.0.0.1:5000'

class Test:
    """
    Test config properties.
    """

    DEBUG = True
    ENV = 'test'
