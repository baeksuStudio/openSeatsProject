from flask import Flask


def create_app() :

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app