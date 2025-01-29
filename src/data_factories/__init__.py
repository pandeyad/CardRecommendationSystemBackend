import importlib
import logging
import os

from src.runner import runner_factory
# Configure logging
logger = logging.getLogger("DataFactories")
logging.basicConfig(level=logging.INFO)

def dynamically_register_all_data_factories(directory):
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

class CrawlerRegistry(type):
    """
    Metaclass to automatically register subclasses of BaseDataFactory.
    """
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        # Avoid registering the BaseDataFactory itself by checking the class name
        if name != 'BaseDataFactory':  # Avoid using BaseDataFactory before it's fully defined
            # Automatically register the subclass with runner_factory
            runner_factory.register(cls)

class BaseDataFactory(metaclass=CrawlerRegistry):

    def run(self):
        raise Exception("Please make a subclass of this for valid data extraction.")

    # Additional methods can go here
