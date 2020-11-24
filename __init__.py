import os

from flask import Flask
from flask_bootstrap import Bootstrap
from support.config import DevelopmentConfig, ProductionConfig

def page_not_found(e):
  return render_template('error/404.html'), 404

def create_app(config_object=DevelopmentConfig()):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from flask_bootstrap import Bootstrap
    Bootstrap(app)

    from routes import bp as routes
    app.register_blueprint(routes)

    return app
