import os
import sys
from .logger import logger


def validate_files(input_file, schema_file):
    """
    Validates the existence of input and schema files and ensures the input file has the correct extension.

    :param input_file: Path to the input YAML file.
    :param schema_file: Path to the schema file.
    :raises SystemExit: If any of the files are invalid or missing.
    """
    # Check if the input file exists
    if not os.path.isfile(input_file):
        logger.error(f"Input file {input_file} does not exist.")
        sys.exit(1)

    # Check if the input file has the correct extension
    if not (input_file.endswith(".yml") or input_file.endswith(".yaml")):
        logger.error(f"Input file {input_file} must have a .yml or .yaml extension.")
        sys.exit(1)

    # Check if the schema file exists
    if not os.path.isfile(schema_file):
        logger.error(f"Schema file {schema_file} not found.")
        sys.exit(1)
