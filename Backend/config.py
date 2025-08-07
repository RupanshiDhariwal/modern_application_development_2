class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SECRET_KEY = None

class ConfigDevelopment(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = 'SECRETKEYhfdskgfhfks'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    SECURITY_TRACKABLE = True

    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'no-reply@a.com'
