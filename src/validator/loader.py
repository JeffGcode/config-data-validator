import json
from pathlib import Path

import yaml


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


     
from .exceptions import ConfigLoadError


def load_config(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise ConfigLoadError(f"Config file not found: {file_path}")

    try:
        if path.suffix in (".yaml", ".yml"):
            return yaml.safe_load(path.read_text())
        elif path.suffix == ".json":
            return json.loads(path.read_text())
        else:
            raise ConfigLoadError("Unsupported config file format")
    except Exception as exc:
        raise ConfigLoadError(str(exc)) from exc
    
    