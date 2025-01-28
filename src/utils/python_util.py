def get_classes_from_file(file_path):
    import ast
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

def load_config():
    from src.utils.config_util import load_configs
    return load_configs()

def get_nested(config, keys, default=None):
    """
    Safely fetch a nested value from a dictionary.

    :param config: The dictionary to fetch from.
    :param keys: A list of keys representing the path to the value.
    :param default: The default value if the keys don't exist.
    :return: The fetched value or the default.
    """
    for key in keys.split('.'):
        if isinstance(config, dict):
            config = config.get(key)
        else:
            return default
    return config if config is not None else default