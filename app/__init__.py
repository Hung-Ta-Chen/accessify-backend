from flask import Flask
from .config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .places.routes import place_blueprint, review_blueprint
    app.register_blueprint(place_blueprint, url_prefix='/api')
    app.register_blueprint(review_blueprint, url_prefix='/api')

    return app
