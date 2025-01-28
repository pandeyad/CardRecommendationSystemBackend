from src.runner import runner_factory

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
