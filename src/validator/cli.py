import argparse
import sys
import logging
from argparse import Namespace
from .loader import load_config
from .exceptions import ConfigLoadError, ValidationError
from .schema import validate_config
from .data_validator import validate_csv
from .db_validator import validate_table_schema, validate_table_data


def main() -> None:
    # ---------- Argument Parser ----------
    parser = argparse.ArgumentParser(description="Config & Data Validator")
    parser.add_argument("--file", help="Path to config file (YAML or JSON)")
    parser.add_argument("--data-file", help="Path to CSV data file")
    parser.add_argument("--db-url", help="Database URL (e.g. sqlite:///data.db)")
    parser.add_argument("--table", help="Table name to validate")
    parser.add_argument("--condition", help="SQL condition for data validation")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging (prints detailed info)",
    )
    args: Namespace = parser.parse_args()

    # ---------- Logging Configuration ----------
    # Set log level based on --verbose flag
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    logger = logging.getLogger(__name__)

    exit_code: int = 0

    # ---------- Config Validation ----------
    if args.file:
        try:
            config_dict = load_config(args.file)
            validated = validate_config(config_dict)
            logger.info("Config valid")
            # Print the validated config (user‑friendly)
            print(validated.model_dump_json(indent=2))
        except (ConfigLoadError, ValidationError) as e:
            logger.error(f"Config error: {e}")
            exit_code = 1

    # ---------- CSV Validation ----------
    if args.data_file:
        try:
            df = validate_csv(args.data_file)
            logger.info("CSV valid")
            print(df.head())
        except ValidationError as e:
            logger.error(f"Data error: {e}")
            exit_code = 1

    # ---------- Database Validation ----------
    if args.db_url and args.table:
        try:
            # Required columns – you could make this configurable later
            required = ["id", "email"]
            validate_table_schema(args.db_url, args.table, required)
            if args.condition:
                validate_table_data(args.db_url, args.table, args.condition)
            logger.info(f"Table '{args.table}' validation passed")
        except ValidationError as e:
            logger.error(f"DB error: {e}")
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
