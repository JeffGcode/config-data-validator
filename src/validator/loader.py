import json
from pathlib import Path
import yaml
from .exceptions import ConfigLoadError


def load_config(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise ConfigLoadError(f"Config file not found: {file_path}")
    try:
        if path.suffix in (".yaml", ".yml"):
            return yaml.safe_load(path.read_text())
        if path.suffix == ".json":
            return json.loads(path.read_text())
        raise ConfigLoadError("Unsupported config format")
    except Exception as exc:
        raise ConfigLoadError(str(exc)) from exc
