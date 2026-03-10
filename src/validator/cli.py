import click
from validator.loader import load_config
from validator.validator import load_schema, validate_config


@click.command()
@click.argument("config_file")
@click.argument("schema_file")
def main(config_file, schema_file):
    config = load_config(config_file)
    schema = load_schema(schema_file)

    try:
        validate_config(config, schema)
        print("✅ Config is valid")
    except Exception as e:
        print("❌ Config validation failed")
        print(e)


if __name__ == "__main__":
    main()
    