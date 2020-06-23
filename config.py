import os
basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    # ...
    # SERVER_NAME = '10.0.0.111:5000'
    DEBUG = False


    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
