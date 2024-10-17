import sys
import yaml
import argparse
from .logger import logger


def get_yml_file(file_path):
    """
    Reads and parses a YAML configuration file.

    Args:
        file_path (str): The path to the YAML file to be read.

    Returns:
        dict: Parsed YAML content as a Python dictionary.

    Functionality:
        - Opens the YAML file at the provided file path in read mode.
        - Uses the PyYAML `safe_load` method to parse the content of the YAML file into a dictionary.
        - Logs the file reading process.

    Error Handling:
        - If an error occurs while opening or reading the YAML file, logs the error message and exits the program.
    """
    try:
        with open(file_path, "r") as file:
            logger.info(f"Reading file {file_path}")
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        logger.error(f"Error reading YAML config file: {e}")
        sys.exit(1)


def parse_arguments():
    """
    Parses command-line arguments for the fstab generator.

    :return: Parsed arguments including input_file and output_file.
    """
    parser = argparse.ArgumentParser(
        usage="python3 fstab_generator.py <input_file> [output_file]",
        description="Generate fstab configuration from a YAML file.",
    )
    parser.add_argument(
        "input_file",
        help="Path to the input YAML file.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="/etc/fstab",
        help="Path to the output fstab file. Defaults to /etc/fstab if not provided.",
    )
    return parser.parse_args()
