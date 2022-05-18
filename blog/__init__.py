import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .auth.views import auth
    app.register_blueprint(auth)

    from .main.views import main
    app.register_blueprint(main)

    return app

