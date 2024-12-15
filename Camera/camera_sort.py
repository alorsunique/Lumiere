# This script should sort the entries in the output folder into their respective years
# Useful only for images with EXIF

import os
import shutil
import sys
from pathlib import Path

from exif import Image


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

    output_dir = resources_dir / "Output"
    if not output_dir.exists():
        os.mkdir(output_dir)

    sorted_dir = resources_dir / "Sorted"
    if not sorted_dir.exists():
        os.mkdir(sorted_dir)

    year_sort(output_dir, sorted_dir)


if __name__ == "__main__":
    main()
