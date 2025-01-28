from flask import Blueprint, jsonify, request
from src.llm.base_model_function import IModelFunction
from src.utils.python_util import load_config
from src import llm



router = Blueprint("api", __name__)
config = load_config()
print(config)
model:IModelFunction = llm.recommendation_app.get_model_instance(config['model']['name'])

@router.route('/chat', methods=['POST'])
def chat():
    print('Executing api : chat')
    print(f"{request.json}")
    user_input = request.json.get("query")
    response = model.recommend(query=user_input)
    return jsonify(response)

@router.route("/api/config", methods=["GET"])
def get_config():
    global config

    """API to fetch app configuration."""
    config = {
        "app": {
            "debug": config["app"]["debug"],
            "host": config["app"]["host"],
            "port": config["app"]["port"]
        }
    }
    return jsonify(config)