from pydantic import BaseModel, Field, ValidationError as PydanticValidationError
from .exceptions import ValidationError


class AppConfig(BaseModel):
    name: str = Field(..., min_length=3)
    environment: str = Field(
        ..., pattern="^(dev|staging|prod)$", description="Deployment environment"
    )
    version: str = Field(default="0.1.0")


def validate_config(config_dict: dict) -> AppConfig:
    """
    Validate a configuration dictionary against the AppConfig schema.

    Args:
        config_dict: Dictionary containing configuration fields.

    Returns:
        AppConfig instance with validated data.

    Raises:
        ValidationError: If the configuration does not match the schema.
    """
    try:
        return AppConfig(**config_dict)
    except PydanticValidationError as e:
        # Convert to our custom ValidationError
        raise ValidationError(str(e)) from e
