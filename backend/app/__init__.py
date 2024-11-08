from flask import Flask
from app.api.routes import api_bp
from app.services.recommendation import FlexibleRecipeRecommendationSystem
from config import Config

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize the recommendation system with both CSV_FILE_PATH and PRECOMPUTED_DIR
    app.recommendation_system = FlexibleRecipeRecommendationSystem(
        app.config['CSV_FILE_PATH'],
        app.config['PRECOMPUTED_DIR']
    )

    app.register_blueprint(api_bp)

    return app