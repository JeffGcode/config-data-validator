import argparse
import sys
from .loader import load_config
from .exceptions import ConfigLoadError, ValidationError
from .schema import validate_config
from .data_validator import validate_csv
from .db_validator import validate_table_schema, validate_table_data


def main():
    parser = argparse.ArgumentParser(description="Config & Data Validator")
    parser.add_argument("--file", help="Path to config file")
    parser.add_argument("--data-file", help="Path to CSV data file")
    parser.add_argument("--db-url", help="Database URL (e.g. sqlite:///data.db)")
    parser.add_argument("--table", help="Table name to validate")
    parser.add_argument("--condition", help="SQL condition for data validation")
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

    if args.db_url and args.table:
        try:
            # For now, require a simple list of required columns
            required = ["id", "email"]
            validate_table_schema(args.db_url, args.table, required)
            if args.condition:
                validate_table_data(args.db_url, args.table, args.condition)
            print(f"✅ Table '{args.table}' validation passed")
        except ValidationError as e:
            print(f"❌ DB error: {e}")
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
