class Default:

    DEBUG = False
    ENV = "production"
    JWT_SECRET_KEY = "default secret key"
    MONGODB_DB = "dawdle"
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PASSWORD = None
    MONGODB_PORT = 27017
    MONGODB_USERNAME = None
    SECRET_KEY = "default secret key"
    SENDER_EMAIL = None
    SENDGRID_API_KEY = None
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"


class Test:

    DEBUG = True
    ENV = "test"
    JWT_SECRET_KEY = "default secret key"
    MONGODB_DB = "dawdle"
    MONGODB_HOST = "mongomock://localhost"
    MONGODB_PASSWORD = None
    MONGODB_PORT = 27017
    MONGODB_USERNAME = None
    SECRET_KEY = "default secret key"
    SENDER_EMAIL = None
    SENDGRID_API_KEY = None
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"
