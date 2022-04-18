from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
Database_Name = "Inscriptiondatabase.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PythonCA70'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Database_Name}'
    db.init_app(app)

    from .inscriptionviews import inscriptionviews
    from .inscriptionauth import inscriptionauth

    app.register_blueprint(inscriptionviews, url_prefix='/')
    app.register_blueprint(inscriptionauth, url_prefix='/')

    from .models import User, Scribble

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'inscriptionauth.Login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + Database_Name):
        db.create_all(app=app)
        print('Inscription Project Database Created!')
