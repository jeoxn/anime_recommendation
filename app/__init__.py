from flask import Flask

def create_app():
    app=Flask(__name__)
    app.secret_key='secretkey'

    from .views import views

    app.register_blueprint(views,url_prefix='/')

    return app