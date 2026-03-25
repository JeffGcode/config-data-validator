import yaml
from pathlib import Path
from typing import Any, Dict, List, Union
from .exceptions import ConfigLoadError


class ValidatorConfig:
    """
    Holds configuration for validation rules.
    Defaults are provided; user can override via YAML file.
    """

    def __init__(self):
        # Default rules for config file validation
        self.config_rules: Dict[str, Any] = {
            "required_fields": ["app_name", "port"],
            "type_checks": {
                "app_name": str,
                "port": int,
                "debug": bool,
            },
            "port_range": (1, 65535),
            "allowed_environments": ["dev", "staging", "prod"],
        }
        # Default rules for CSV validation
        self.csv_rules: Dict[str, Any] = {
            "required_columns": ["id", "email", "age"],
            "email_validation": True,
        }
        # Default rules for database validation
        self.db_rules: Dict[str, Any] = {
            "required_columns": ["id", "email"],
        }

    def load_from_file(self, file_path: str) -> None:
        """Load configuration from a YAML file and update settings."""
        path = Path(file_path)
        if not path.exists():
            raise ConfigLoadError(f"Config file not found: {file_path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise ConfigLoadError(f"Failed to parse YAML: {e}")

        if not data:
            return  # Empty file, keep defaults

        # Merge config section
        if "config" in data:
            cfg = data["config"]
            if "required_fields" in cfg:
                self.config_rules["required_fields"] = cfg["required_fields"]
            if "type_checks" in cfg:
                # Convert string type names to actual Python types
                type_map = {"str": str, "int": int, "bool": bool}
                self.config_rules["type_checks"] = {
                    k: type_map[v] for k, v in cfg["type_checks"].items()
                }
            if "port_range" in cfg:
                self.config_rules["port_range"] = tuple(cfg["port_range"])
            if "allowed_environments" in cfg:
                self.config_rules["allowed_environments"] = cfg["allowed_environments"]

        # Merge CSV section
        if "csv" in data:
            csv = data["csv"]
            if "required_columns" in csv:
                self.csv_rules["required_columns"] = csv["required_columns"]
            if "email_validation" in csv:
                self.csv_rules["email_validation"] = csv["email_validation"]

        # Merge DB section
        if "db" in data:
            db = data["db"]
            if "required_columns" in db:
                self.db_rules["required_columns"] = db["required_columns"]

    def get_config_rules(self) -> Dict[str, Any]:
        """Return rules for validating configuration files."""
        return self.config_rules

    def get_csv_rules(self) -> Dict[str, Any]:
        """Return rules for validating CSV files."""
        return self.csv_rules

    def get_db_rules(self) -> Dict[str, Any]:
        """Return rules for validating database tables."""
        return self.db_rules