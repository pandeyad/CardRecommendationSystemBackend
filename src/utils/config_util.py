import os
import yaml
from pathlib import Path
from sysconfig import get_paths

def load_configs(check_duplicates=True):
    """
    Load and merge all YAML configuration files into a single dictionary at the top level.

    :param check_duplicates: If True, raise an error on duplicate keys. If False, overwrite existing keys.
    :return: A single merged dictionary with configurations.
    """
    merged_config = {}
    try:
        # Get the installation directory for 'data_files'
        data_dir = Path(get_paths()["data"]) / "configurations"

        # Ensure the directory exists
        if not data_dir.is_dir():
            raise FileNotFoundError(f"Configuration directory not found: {data_dir}")

        # Iterate through all YAML files in the directory
        for file in data_dir.iterdir():
            if file.suffix.lower() in [".yaml", ".yml"]:  # Only process YAML files
                try:
                    with file.open("r") as f:
                        config_data = yaml.safe_load(f)
                        if not isinstance(config_data, dict):
                            raise ValueError(f"File {file.name} does not contain a valid dictionary.")

                        # Check for duplicate keys
                        if check_duplicates:
                            for key in config_data:
                                if key in merged_config:
                                    raise ValueError(f"Duplicate key '{key}' found in file: {file.name}")

                        # Merge configurations
                        merged_config.update(config_data)

                except Exception as e:
                    print(f"Warning: Failed to load {file.name} - {e}")

    except Exception as e:
        raise RuntimeError(f"Error loading configurations: {e}")

    return merged_config
