from pydantic import BaseModel, Field, ValidationError


class AppConfig(BaseModel):
    name: str = Field(..., min_length=3, description="Application name")
    environment: str = Field(
        ..., pattern="^(dev|staging|prod)$", description="Deployment environment"
    )
    version: str = Field(default="0.1.0", description="Semantic version")


def validate_config(config_dict: dict) -> AppConfig:
    """Validate a configuration dictionary against the schema."""
    try:
        return AppConfig(**config_dict)
    except ValidationError as e:
        raise e
