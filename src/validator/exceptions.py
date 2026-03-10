class ConfigLoadError(Exception):
    """Raised when a configuration file cannot be loaded."""


class ValidationError(Exception):
    """Raised when validation rules fail."""
    