import argparse
import sys
from .loader import load_config
from .exceptions import ConfigLoadError
from .schema import validate_config
from pydantic import ValidationError  # <-- add import

def main():
    parser = argparse.ArgumentParser(description="Config Data Validator")
    parser.add_argument("--file", required=True, help="Path to config file")
    args = parser.parse_args()

    try:
        config_dict = load_config(args.file)
        validated = validate_config(config_dict)
        print("✅ Config loaded and validated successfully")
        print(validated.model_dump_json(indent=2))
        sys.exit(0)
    except (ConfigLoadError, ValidationError) as err:
        print(f"❌ Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()

    