# This script should sort the entries in the output folder into their respective years
# Useful only for images with EXIF

import os
import shutil
import sys
from pathlib import Path

import yaml
from exif import Image


# Sorts the images by year
def year_sort(output_dir, sorted_dir):
    count = 0

    for image_file in output_dir.iterdir():
        count += 1
        print(f"Current Count: {count} | {image_file.name}")

        opened_image = open(image_file, 'rb')
        image_object = Image(opened_image)
        opened_image.close()

        # Gets the year of the image here
        datetime_chunk = image_object.datetime.split(" ")
        date_chunk = datetime_chunk[0].split(":")

        image_year = int(date_chunk[0])

        move_folder = sorted_dir / f"{image_year}"
        if not move_folder.exists():
            os.mkdir(move_folder)

        shutil.move(image_file, move_folder)


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


# Main
def main():
    config_file_name = 'Lumiere_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])

    # Initializes the folders if they are not present
    output_dir = resources_dir / "Output"
    if not output_dir.exists():
        os.mkdir(output_dir)

    sorted_dir = resources_dir / "Sorted"
    if not sorted_dir.exists():
        os.mkdir(sorted_dir)

    year_sort(output_dir, sorted_dir)


if __name__ == "__main__":
    main()
