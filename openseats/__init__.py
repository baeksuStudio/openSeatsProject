from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app() :
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # Blueprint
    from .views import main_views, group_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(group_views.bp)

    return app