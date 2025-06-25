# This script should rename images based on their EXIF data

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml
from exif import Image


# Checks if the files in input has EXIF
# If yes, moved to output
def EXIF_check(input_dir, output_dir):
    for entry in input_dir.iterdir():
        if entry.is_file():
            opened_file = open(entry, 'rb')

            try:
                image_object = Image(opened_file)
                jpg_check = True
            except:
                jpg_check = False

            opened_file.close()

            if jpg_check and image_object.has_exif:
                image_output_path = output_dir / entry.name
                shutil.move(entry, image_output_path)


# Preliminary rename based on current time
def preliminary_name(output_dir):
    image_count = 0

    for image_file in output_dir.iterdir():
        image_count += 1
        print(f"Preliminary Renaming: {image_file.name}")

        file_suffix = image_file.suffix

        # Adds a time filter to make sure all files have unique preliminary names
        time_filter = datetime.now()
        time_filter = time_filter.strftime("%H%M%S")

        new_image_name = f"{str(image_count).zfill(8)}{time_filter}{file_suffix}"
        new_image_path = output_dir / new_image_name

        os.rename(image_file, new_image_path)


# Proper rename based on EXIF data
def proper_rename(output_dir):
    image_count = 0
    same_image_count = 0

    for image_file in output_dir.iterdir():
        print(f"Current Renaming: {image_file.name}")

        file_suffix = image_file.suffix

        opened_image = open(image_file, 'rb')
        image_object = Image(opened_image)
        opened_image.close()

        # Get the datetime property of the image
        datetime_chunk = image_object.datetime.split(" ")
        date_chunk = datetime_chunk[0].split(":")
        time_chunk = datetime_chunk[1].split(":")

        rename_date = ""
        rename_time = ""

        for chunk in date_chunk:
            rename_date += chunk
        for chunk in time_chunk:
            rename_time += chunk

        new_image_name = f"{rename_date}_{rename_time}_{image_object.model}{file_suffix}"
        new_image_path = output_dir / new_image_name

        # This section checks for duplicates
        if new_image_path.exists():
            print("Renaming Same Images")
            while True:
                same_image_count += 1
                same_new_name = f"{rename_date}_{rename_time}_{image_object.model}_{same_image_count}{file_suffix}"
                same_path = output_dir / same_new_name
                if not same_path.exists():
                    new_image_path = same_path
                    break
            os.rename(image_file, new_image_path)
            same_image_count = 0
        else:
            os.rename(image_file, new_image_path)

        image_count += 1


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
    input_dir = resources_dir / "Input"
    if not input_dir.exists():
        os.mkdir(input_dir)

    output_dir = resources_dir / "Output"
    if not output_dir.exists():
        os.mkdir(output_dir)

    # Renaming is done here
    EXIF_check(input_dir, output_dir)
    preliminary_name(output_dir)
    proper_rename(output_dir)


if __name__ == "__main__":
    main()
