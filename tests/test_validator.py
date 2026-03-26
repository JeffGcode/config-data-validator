import pytest
from src.validator.schema import validate_config
from src.validator.exceptions import ValidationError  # ← fixed import


def test_valid_config():
    config = {"name": "myapp", "environment": "dev", "version": "1.0.0"}
    result = validate_config(config)
    assert result.name == "myapp"
    assert result.environment == "dev"
    assert result.version == "1.0.0"


def test_invalid_config_missing_field():
    config = {"name": "myapp"}  # missing environment
    with pytest.raises(ValidationError):
        validate_config(config)


def test_invalid_config_bad_environment():
    config = {"name": "myapp", "environment": "bad", "version": "1.0.0"}
    with pytest.raises(ValidationError):
        validate_config(config)
