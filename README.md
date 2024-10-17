# Fstab Generator Script

This Python script reads an input YAML file, validates it against a provided JSON schema, and generates an `fstab` configuration file. The script ensures the correct syntax and structure for the `fstab` file.

## Usage
  > **ℹ️ Info:**  
  > `Python 3.8` or later should be installed on your machine.

1. **Install Python Virtual Environment Module**:
    ```bash
    python3 -m pip install virtualenv
    ```
2. **Create Python Virtual Environment**:
    ```bash
    python3 -m venv .venv
    ```
3. **Activate the Python Virtual Environment**:
    ```bash
    source .venv/bin/activate
    ```
4. **Install Python Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```
5. **Running the fstab Generator Script**:
    ```bash
    # Usage: python3 fstab_generator.py <input_file> [output_file]

    # Generate fstab configuration from a YAML file.

    # positional arguments:
      # input_file   Path to the input YAML file.
      # output_file  Path to the output fstab file. Defaults to /etc/fstab if not provided.

    # options:
      # -h, --help   show this help message and exit

    # Example 1
    python3 fstab_generator.py ./examples/fstab_config_1.yml fstab1
    
    # Example 2
    python3 fstab_generator.py ./examples/fstab_config_2.yml fstab2

    # Example 2 (using default output_file path /etc/fstab)
    sudo python3 fstab_generator.py ./examples/fstab_config_2.yml
    ```

## Features

- **YAML Input**: Parses a YAML file containing device configuration details.
- **Validation**: Validates the input YAML file against a predefined JSON schema to ensure correct structure and mandatory fields.
- **Fstab Generation**: Generates a valid `fstab` file for mounting devices with the necessary options, including NFS-specific mounts and optional fields like `dump` and `fsck`.


## Input YAML Format:
   - The input YAML should define devices with attributes:
      - `mount` (required)
      - `type` (required)
      - `options` (optional)
      - `export` (optional)
      - `dump` (optional)
      - `fsck` (optional)

  **Note**:
  1. The `mount` and `type` fields are required and do not have default values in the script.
  2. The `options` field is optional; if not specified, it will default to the value `defaults` and if specified it will be concatenated with value `defaults`.
        - For example: 
            1. If `options` are specified such as `noexec` and `nosuid` the options field in the fstab will look like this `defaults,noexec,nosuid`.
            2. If `options` are not specified then the options field in the fstab will look like this `defaults`.
  3. The `export` field is mandatory only when the `type` field is set to `nfs`; otherwise, it can be left out.
  4. Both `dump` and `fsck` are optional fields; if they are not specified, they will default to `0`.
   
   **Examples**:

  ```yaml
  ---
  # Example 1
  fstab:
    /dev/sda1:
      mount: /boot
      type: xfs
    /dev/sda2:
      mount: /
      type: ext4
    /dev/sdb1:
      mount: /var/lib/postgresql
      type: ext4
      root-reserve: 10%
    192.168.4.5:
      mount: /home
      export: /var/nfs/home
      type: nfs
      options:
        - noexec
        - nosuid
  ---
  # Example 2
  fstab:
    /dev/sda1:
      mount: /boot
      type: xfs
      dump: 0
      fsck: 2
    /dev/sda2:
      mount: /
      type: ext4
    /dev/sdb1:
      mount: /var/lib/postgresql
      type: ext4
      root-reserve: 10%
    192.168.4.5:
      mount: /home
      export: /var/nfs/home
      type: nfs
      options:
        - noexec
        - nosuid
  ```

## Schema Validation:
  - A `schemas/fstab_config_schema.json` file is used as schema to validate the YAML input.
  - If the input YAML file doesn't conform to the JSON schema, the script will log the validation errors and stop execution.

## Logs

- The script logs actions like reading files, validation status, and errors to the console for better tracking.

## Error Handling

- If the YAML file is invalid, the script logs an error and terminates.
- If the `fstab` file generation fails, it logs the issue and provides a stack trace for debugging.

## Example Output

An example generated `fstab` entry:

```bash
/dev/sda1  /boot  xfs  defaults  0  0
/dev/sda2  /  ext4  defaults  0  0
/dev/sdb1  /var/lib/postgresql  ext4  defaults  0  1
192.168.4.5:/var/nfs/home  /home  nfs  defaults,noexec,nosuid  0  0
```

## Observations and Thoughts

In reviewing the task requirements and the provided YAML structure, I noted that the original YAML file did not include fields for `dump` and `fsck`. However, I have included these fields in my implementation to enhance the flexibility of the generated `fstab` configuration.

### Explanation of Additional Fields

- **`dump`**: This field indicates whether the file system should be backed up by the `dump` command. By default, I have set it to `0` (disabled) unless specified otherwise in the YAML input.
  
- **`fsck`**: This field specifies the order in which the file system checks are done at boot time. A value of `0` means the file system will not be checked. Similar to `dump`, this field defaults to `0` unless the user provides a different value in the YAML.

These additions provide users with the option to customize these settings as needed while still adhering to the structure provided in the original task. If you want to set values for `dump` and `fsck`, you can do so directly in the YAML file. If not specified, the script will gracefully fall back to the default values.

This way, the structure of the YAML file remains consistent with the original task while offering additional configuration options.

### Handling of `root-reserve`

One of the device configurations in the provided YAML file included a field named `root-reserve`. It’s important to note that this field cannot be set using the `fstab` configuration file. The `root-reserve` percentage is typically configured using the `tune2fs` command, which adjusts the reserved block percentage for a file system. 

For example, to set 10% for the root file system on `/dev/sdb1`, the command would be:
```bash
# Example: tune2fs -m <percentage> <device>
tune2fs -m 10 /dev/sdb1
```

Since root-reserve is not a standard entry in the /etc/fstab file, I have opted to ignore this field while constructing the fstab file. However, I have logged a warning indicating that the root-reserve is required for the device. The warning suggests running the following command after the mount to set the appropriate reserve percentage:
```bash
root-reserve is required for device /dev/sdb1, try this command after the mount: tune2fs -m 10 /dev/sdb1
```

I recognize that it may be useful to develop a separate utility that utilizes the same YAML structure to manage the root-reserve setting. Implementing such functionality would be beyond the scope of this assignment, but it could be a valuable addition in future enhancements.