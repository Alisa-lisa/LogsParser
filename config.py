class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'change_me'
    UPLOAD_FOLDER = 'application/log_parser/upload'
    COMPRESSION_EXTENSIONS = [".xz", ".tar", ".zip"]
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/visualizer"


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    pass


class LocalDevelopment(Config):
    DEBUG = True
    TESTING = True
