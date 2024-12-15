# This script should rename images based on their EXIF data

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from exif import Image


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


def main():
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    # Change working directory to project directory
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    with open("Resources_Path.txt", "r") as read_text:
        lines = read_text.readlines()

    resources_dir = Path(lines[0].replace('"', ''))

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
