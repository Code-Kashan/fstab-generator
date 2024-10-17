import sys
import json
from jsonschema.exceptions import ValidationError
from jsonschema import validate
from .logger import logger


def validate_yml_file(yml_file, schema_file_path):
    """
    Validates a YAML file against a given JSON schema.

    Args:
        yml_file (dict): The parsed YAML file content to be validated.
        schema (dict): The JSON schema that defines the structure and validation rules.

    Functionality:
        - Uses the `jsonschema` library's `validate` function to check if the YAML file content adheres to the specified schema.
        - Logs a success message if validation passes.

    Error Handling:
        - If the YAML file fails schema validation, catches `ValidationError`, logs the specific validation error message, and the JSON path of the issue.
        - If any other exception occurs during validation, logs the error and exits the program.
    """
    try:
        with open(schema_file_path, "r") as schema_file:
            schema = json.load(schema_file)
        logger.info(f"Validating schema for input file")
        validate(instance=yml_file, schema=schema)
        logger.info(f"Validation succeeded")
    except ValidationError as err:
        logger.error(f"Validation failed: {err.message}")
        logger.error(f"Validation error occured at JSON Path: {err.json_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error processing file while validating: {str(e)}")
        sys.exit(1)
