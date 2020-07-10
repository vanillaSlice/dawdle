class Default:

    CONTACT_EMAIL = None
    DEBUG = False
    ENV = "production"
    JWT_SECRET_KEY = "default secret key"
    MONGODB_HOST = "127.0.0.1"
    SECRET_KEY = "default secret key"
    SENDER_EMAIL = None
    SENDGRID_API_KEY = None
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"


class Test:

    CONTACT_EMAIL = None
    DEBUG = True
    ENV = "test"
    JWT_SECRET_KEY = "default secret key"
    MONGODB_HOST = "mongomock://localhost"
    SECRET_KEY = "default secret key"
    SENDER_EMAIL = None
    SENDGRID_API_KEY = None
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"
