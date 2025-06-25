# This script should downscale the image and convert it to grayscale for faster filtering

import os
import shutil
import sys
from pathlib import Path

import cv2
import yaml


# Function to find the project directory
# Uses the config file as marker
def find_project_root(script_path, marker):
    current_path = script_path
    while not (current_path / marker).exists():
        # If block checks for parent of current path
        # If it cannot go up any further, base directory is reached
        if current_path.parent == current_path:
            raise FileNotFoundError(f"Could not find '{marker}' in any parent directories.")

        current_path = current_path.parent

    # If it exits the while loop, marker was found
    return current_path


def main():
    config_file_name = 'Lumiere_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])

    input_dir = resources_dir / "Input"
    create_dir = resources_dir / "Create"

    # Reset the Create folder
    if create_dir.exists():
        shutil.rmtree(create_dir)
    os.mkdir(create_dir)

    # Resize dimension

    new_height = 128
    new_width = 128

    count = 0

    for entry in input_dir.iterdir():
        if entry.is_file():
            count += 1
            print(f"{count} | {entry.name}")

            try:
                source_image = cv2.imread(str(entry))
                source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

                resize_image = cv2.resize(source_image, (new_width, new_height))

                resize_path = create_dir / entry.name
                cv2.imwrite(str(resize_path), resize_image)
                cv2.destroyAllWindows()
            except:
                print("Could not resize")


if __name__ == "__main__":
    main()
