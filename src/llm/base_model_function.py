from src.llm import recommendation_app, BaseModelFunction


class ModelRegistry(type):
    """
    Metaclass to automatically register subclasses of BaseModelFunction.
    """
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        # Avoid registering the BaseModelFunction itself
        if name not in ['IModelFunction', 'BaseModelFunction']:
            # Get model_name from class level (either from a decorator or directly defined)
            model_name = getattr(cls, '__model_name__', None) or name.lower()
            # Automatically register the subclass with RecommendationApp
            recommendation_app.register_model(cls, model_name)



class IModelFunction(BaseModelFunction, metaclass=ModelRegistry):

    def get_config(self):
        return self.config.get('model', {}).get('configuration', {}).get(self.__getattribute__('__model_name__'), {})

    def prepare_model(self):
        raise Exception(
            "Invoking unregistered model. Please register a model and implement the prepare_model method to train the model.")

    def recommend(self, query):
        raise Exception(
            "Invoking unregistered model. Please register a model and implement the recommend method to use the same.")