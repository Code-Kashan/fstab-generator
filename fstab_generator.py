import traceback
from helpers.schema_validator import validate_yml_file
from helpers.parse import get_yml_file
from helpers.parse import parse_arguments
from helpers.files_validator import validate_files
from helpers.logger import logger

SCHEMA_FILE_PATH = "schemas/fstab_config_schema.json"
field_options_default = "defaults"
field_dump_default = "0"
field_fsck_default = "0"


def populate_fstab(input_file_path, output_file_path):
    """
    Generates an fstab configuration file based on the provided YAML configuration.

    Args:
        config (dict): A dictionary containing device configurations, including fields like 'mount', 'type',
                       'options', 'export', 'dump', and 'fsck'.
        output_file_path (str): The path where the generated fstab file should be written.

    Functionality:
        - Iterates over the devices in the configuration to extract relevant fields for each device.
        - Constructs the necessary fields for fstab syntax, including 'mount point', 'type', 'options', 'dump', and 'fsck'.
        - For NFS devices, appends the 'export' field to the device name.
        - Adds default values for optional fields 'dump' and 'fsck' if they are not provided.
        - Combines the fields into the required fstab format and writes them to the output file.

    Logging:
        - Logs the start of the fstab generation process.
        - Logs the generation of configuration for each device.
        - Logs the completion of writing the generated configuration to the output file.

    Error Handling:
        - If an error occurs during the fstab generation process, logs the error and prints the stack trace.
    """
    logger.info(f"Generating fstab config")
    list_of_lines = []
    try:
        config = get_yml_file(input_file_path)
        for _, devices in config.items():
            for device, device_config in devices.items():
                logger.info(f"Generating config for device {device}")
                field_device = device
                field_mount_point = device_config["mount"]
                field_fs_type = device_config["type"]
                field_options = field_options_default
                field_export = device_config.get("export")
                field_dump = device_config.get("dump", field_dump_default)
                field_fsck = device_config.get("fsck", field_fsck_default)

                if field_fs_type == "nfs":
                    field_device = field_device + ":" + field_export

                if "options" in device_config:
                    field_options = (
                        field_options + "," + ",".join(device_config["options"])
                    )

                list_of_lines.append(
                    f"{field_device}  {field_mount_point}  {field_fs_type}  {field_options}  {field_dump}  {field_fsck}"
                )

                if "root-reserve" in device_config:
                    logger.warning(
                        f"root-reserve is required for device {device}, try this command after the mount: tune2fs -m {device_config['root-reserve'][:-1]} {device}"
                    )

        logger.info(f"Writing the generated config to file {output_file_path}")
        with open(output_file_path, "w") as file:
            file.write("\n".join(list_of_lines))
            file.write("\n")

    except Exception as e:
        logger.error("An error occured while constructing the fstab file !")
        traceback.print_exc()


def main():
    args = parse_arguments()
    validate_files(args.input_file, SCHEMA_FILE_PATH)
    validate_yml_file(get_yml_file(args.input_file), SCHEMA_FILE_PATH)
    populate_fstab(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
