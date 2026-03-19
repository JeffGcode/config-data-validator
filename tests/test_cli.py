import pytest
from src.validator.schema import validate_config
from pydantic import ValidationError


def test_placeholder():
    assert True


def test_invalid_config():
    bad = {"name": "ab", "environment": "bad"}
    with pytest.raises(ValidationError):
        validate_config(bad)
