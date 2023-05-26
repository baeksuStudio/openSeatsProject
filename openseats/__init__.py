from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app() :
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    # 파일 저장 경로 설정
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads', 'img')
    app.config['USER_PROFILE'] = os.path.join(basedir, 'static', 'img', 'profile')

    # ORM
    db.init_app(app)
    
    migrate.init_app(app, db)
    from . import models


    # Blueprint
    from .views import main_views, group_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(group_views.bp)
    app.register_blueprint(auth_views.bp)

    return app