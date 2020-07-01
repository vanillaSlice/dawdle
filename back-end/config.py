class Default:

    DEBUG = False
    ENV = "production"
    SECRET_KEY = "default secret key"
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"


class Test:

    DEBUG = True
    ENV = "test"
    SECRET_KEY = "default secret key"
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"
