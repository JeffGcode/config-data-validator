import argparse
import sys
from .loader import load_config
from .exceptions import ConfigLoadError, ValidationError
from .schema import validate_config
from .data_validator import validate_csv

def main():
    parser = argparse.ArgumentParser(description="Config & Data Validator")
    parser.add_argument("--file", help="Path to config file")
    parser.add_argument("--data-file", help="Path to CSV data file")
    args = parser.parse_args()

    exit_code = 0

    if args.file:
        try:
            config_dict = load_config(args.file)
            validated = validate_config(config_dict)
            print("✅ Config valid")
            print(validated.model_dump_json(indent=2))
        except (ConfigLoadError, ValidationError) as e:
            print(f"❌ Config error: {e}")
            exit_code = 1

    if args.data_file:
        try:
            df = validate_csv(args.data_file)
            print("✅ CSV valid")
            print(df.head())
        except ValidationError as e:
            print(f"❌ Data error: {e}")
            exit_code = 1

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
    

    