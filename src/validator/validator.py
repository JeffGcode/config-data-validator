import json
from jsonschema import validate


def load_schema(path):
    with open(path, "r") as f:
        return json.load(f)


def validate_config(config, schema):
    validate(instance=config, schema=schema)
    