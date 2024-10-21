import json


def load_config(filename='config.json'):
    """Load configuration from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)