import json
import re
from pathlib import Path

def read_config_file(config_file: Path):
    """
    Reads the config.txt file and returns a dict of the values
    :param config_file: The Path object of the config.txt file
    :return: A dict of the config values
    """
    config_dict = {}
    with open(file = config_file, mode = "r", encoding = "utf-8") as opened:
        lines = opened.readlines()
        for line in lines:
            # Comment line
            if re.match(string = line, pattern = " *#.*"):
                continue
            # Blank line
            elif re.match(string = line, pattern = "^ *$"):
                continue
            # Config line
            elif re.match(string = line, pattern = "^ *([^ ]*) *= *(\d*) *$"):
                matched = re.match(string = line, pattern = "^ *([^ ]*) *= *(\d*) *$")
                config_dict[matched.group(1)] = int(matched.group(2))
            # Assume everything else is an error
            else:
                line_stripped = line.replace("\n", "")
                print(f"ERROR: Invalid line in config.txt:\n{line_stripped}\nExiting.")
                exit(-1)
    return config_dict


if __name__ == '__main__':
    # Load config
    config_file = Path("config.txt")
    if not config_file.exists():
        print("ERROR: config.txt does not exist. Exiting.")
        exit(-1)
    config_dict = read_config_file(config_file = config_file)
    print(json.dumps(config_dict, indent = 4))

