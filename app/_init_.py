import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_mail import Mail
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from elasticsearch import Elasticsearch
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
login = LoginManager(app)
moment = Moment(app)
app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) \
    if app.config['ELASTICSEARCH_URL'] else None
babel = Babel(app)

login.login_view = 'login' #view function that handles login
login.login_message = 'Please log in to access this page.'

from app import routes, models, errors

#... Error Handling
if not app.debug:
    #... log errors by email
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    #..maintain a log file for the application  
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')