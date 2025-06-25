import os
from pathlib import Path

import yaml

if __name__ == "__main__":
    config_file_name = 'Lumiere_config.yaml'
    config_file_path = config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])

    print(f"Resources Directory: {resources_dir}")

    # Creates Resources Directory
    if not resources_dir.exists():
        os.mkdir(resources_dir)
