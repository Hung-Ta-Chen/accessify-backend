from flask import Flask, jsonify
from .config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from pymongo import MongoClient

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # for cross platform

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize MongoDB connection
    mongo_client = MongoClient(app.config['MONGO_URI'])
    mongo_db = mongo_client['db_name']

    from .places.routes import place_blueprint, review_blueprint
    app.register_blueprint(place_blueprint, url_prefix='/api')
    app.register_blueprint(review_blueprint, url_prefix='/api')

    # Global error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found', 'message': str(error)}), 404

    return app
