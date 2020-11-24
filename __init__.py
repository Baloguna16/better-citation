import os

from flask import Flask
from flask_bootstrap import Bootstrap
from support.config import DevelopmentConfig, ProductionConfig

def page_not_found(e):
  return render_template('error/404.html'), 404

def internal_server(e):
  return render_template('error/500.html'), 500

def create_app(config_object=ProductionConfig()):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from flask_bootstrap import Bootstrap
    Bootstrap(app)

    from routes import bp as routes
    app.register_blueprint(routes)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server)
    return app
