from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy()
db_name = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bdhbhuybdsh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views , url_prefix='/')
    app.register_blueprint(auth , url_prefix='/')

    from .models import User, Note
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_views = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_db(app):
    if not path.exists('project/'+ db_name):
        db.create_all(app=app)
        print("Database Created Successfully")
