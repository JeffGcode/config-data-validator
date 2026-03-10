from validator.loader import load_config
from validator.validator import load_schema, validate_config


def test_config_validation():
    config = load_config("samples/config.yaml")
    schema = load_schema("samples/schema.json")

    validate_config(config, schema)
    