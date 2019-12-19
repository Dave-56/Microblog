import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # secret key env var for wtf-forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #TEMPLATES_AUTO_RELOAD = True
    
    # ... DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #...Send Errors to mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT= int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['pemakenemi56@gmail.com']

    #...Pagination
    POSTS_PER_PAGE = 3

    #...Elastic search
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or None

    #... heroku, to log to stdout
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
