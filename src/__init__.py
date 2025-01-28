from flask import Flask, request, jsonify

from src.job_scheduler import JobIntervalScheduler
from src.utils.python_util import load_config
from flask_cors import CORS  # Import CORS

def create_app():
    # Create a Flask app instance
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    # Load configuration from YAML file
    load_config()
    # Register blueprints or routes
    from src.routes import router
    app.register_blueprint(router)
    return app

def scheduled_job_runner():
    JobIntervalScheduler().schedule()