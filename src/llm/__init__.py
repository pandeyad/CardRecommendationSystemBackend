import logging
from abc import abstractmethod

from src.utils.python_util import load_config
from pathlib import Path

# Configure logging
logger = logging.getLogger("RecommendationApp")
logging.basicConfig(level=logging.INFO)


import os
import importlib

def dynamically_register_all_models(directory):
    """
    Dynamically imports all classes and methods from Python files in the specified directory
    and its nested subdirectories.

    :param directory: Path to the root directory to scan for Python files.
    :return: A dictionary with module names as keys and their classes/methods as values.
    """
    results = {}
    logging.info(f"Importing modules from {directory}")

    # Traverse the directory recursively
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Get the full path to the Python file
                file_path = os.path.join(root, file)
                try:
                    # Dynamically import the module
                    logger.info(f"Importing from module from file path : {file_path}")
                    # Ensure that model file name and class name are same
                    importlib.import_module(str(file_path).replace('.py', '').replace('/', '.'))
                except Exception as e:
                    print(f"Failed to import modules from {file_path} : {e}")
    return results


class BaseModelFunction:

    def __init__(self):
        self.config = load_config()
        self.files = [f.as_posix() for f in Path(self.config['data']['base_path']).rglob('*') if f.is_file()]

    @abstractmethod
    def prepare_model(self):
        raise Exception(
            "Invoking unregistered model. Please register a model and implement the prepare_model method to train the model.")

    @abstractmethod
    def recommend(self, query):
        raise Exception(
            "Invoking unregistered model. Please register a model and implement the recommend method to use the same.")



class RecommendationApp:
    _singleton_instance = None  # Private class variable for singleton
    registered_models = {}  # Dictionary to store model name -> instance mapping

    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super(RecommendationApp, cls).__new__(cls, *args, **kwargs)
        return cls._singleton_instance

    @classmethod
    def register_model(cls, model_class, model_name):
        """
        Automatically register a subclass of BaseModelFunction.
        """
        # model_name = model_class.__name__.lower()  # Use the class name as the model name
        if model_name in cls.registered_models:
            logger.warning(f"Model '{model_name}' is already registered and will be overwritten.")

        if not issubclass(model_class, BaseModelFunction):
            raise Exception("Recommendation app to be registered must be a subclass of BaseModelFunction")


        # Create an instance of the model and register it
        try:
            instance = model_class()
            logger.info(f"Registering Model : {model_name}")
            cls.registered_models[model_name] = instance
        except Exception as e:
            raise RuntimeError(f"Failed to register or prepare model '{model_name}': {e}")

    @classmethod
    def refresh_model_data(cls):
        """
        Refresh data for all registered models.
        """
        if not cls.registered_models:
            logger.info("No models registered.")
            return
        # Can potentially use multithreading here
        for model_name, instance in cls.registered_models.items():
            try:
                logger.info(f"Refreshing data for model: {model_name}")
                instance.prepare_model()
            except Exception as e:
                logger.error(f"Error refreshing model '{model_name}': {e}")

    @classmethod
    def get_model_instance(cls, name: str):
        """
        Retrieves the instance associated with the given model name.
        """
        instance = cls.registered_models.get(name.lower())
        if instance:
            return instance
        else:
            raise ValueError(f"Model '{name}' not found.")

    @classmethod
    def get_all_models(cls):
        """
        Returns all registered models and their instances.
        """
        return cls.registered_models

# Singleton instance
recommendation_app = RecommendationApp()


