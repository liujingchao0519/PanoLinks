import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()

#oauth = OAuth(myapp)

def create_app(config_class=Config):


    myapp = Flask(__name__)
    myapp.config.from_object(config_class)

    db.init_app(myapp)
    migrate.init_app(myapp, db)
    bootstrap.init_app(myapp)
    login.init_app(myapp)
    mail.init_app(myapp)


    from myapp.errors import bp as errors_bp
    myapp.register_blueprint(errors_bp)

    from myapp.auth import bp as auth_bp, routes

    myapp.register_blueprint(auth_bp, url_prefix='/auth')

    from myapp.main import bp as main_bp
    myapp.register_blueprint(main_bp)


    if not myapp.debug and not myapp.testing:
        if myapp.config['MAIL_SERVER']:
            auth = None
            if myapp.config['MAIL_USERNAME'] or myapp.config['MAIL_PASSWORD']:
                auth = (myapp.config['MAIL_USERNAME'], myapp.config['MAIL_PASSWORD'])
            secure = None
            if myapp.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(myapp.config['MAIL_SERVER'], myapp.config['MAIL_PORT']),
                fromaddr='no-reply@' + myapp.config['MAIL_SERVER'],
                toaddrs=myapp.config['ADMINS'], subject='Panolinks Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            myapp.logger.addHandler(mail_handler)

    return myapp

from myapp import models





