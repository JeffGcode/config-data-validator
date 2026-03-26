import pytest
from src.validator.schema import validate_config
from src.validator.exceptions import ValidationError  # ← fixed import


def test_placeholder():
    assert True


def test_invalid_config():
    bad = {"name": "ab", "environment": "bad"}
    with pytest.raises(ValidationError):
        validate_config(bad)
