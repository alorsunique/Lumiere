# This script should rename edited photos
# Both PNG and JPG are supported

import os
import sys
import time
from datetime import datetime
from pathlib import Path

from exif import Image


def preliminary_name(input_dir):
    image_count = 0

    for image_file in input_dir.iterdir():
        image_count += 1
        print(f"Preliminary Renaming: {image_file.name}")

        file_suffix = image_file.suffix

        # Adds a time filter to make sure all files have unique preliminary names
        time_filter = datetime.now()
        time_filter = time_filter.strftime("%H%M%S")

        new_image_name = f"{str(image_count).zfill(8)}{time_filter}{file_suffix}"
        new_image_path = input_dir / new_image_name

        os.rename(image_file, new_image_path)


def proper_rename(input_dir):
    image_count = 0
    same_image_count = 0

    for image_file in input_dir.iterdir():
        print(f"Current Renaming: {image_file.name}")

        file_suffix = image_file.suffix

        valid_file_check = True

        if file_suffix == ".png":
            # Performs PNG specific modification
            # For PNG, no EXIF so the modification time is used

            mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(image_file)))

            datetime_chunk = mod_time.split(" ")
            date_chunk = datetime_chunk[0].split(":")
            time_chunk = datetime_chunk[1].split(":")

            rename_date = ""
            rename_time = ""

            for chunk in date_chunk:
                rename_date += chunk
            for chunk in time_chunk:
                rename_time += chunk

            new_name = f"Edit_{rename_date}_{rename_time}{file_suffix}"

        elif file_suffix == ".jpg" or file_suffix == ".jpeg":

            opened_file = open(image_file, 'rb')
            image_object = Image(opened_file)
            opened_file.close()

            # Checks for EXIF
            if image_object.has_exif:

                # Image might have EXIF but has no datetime entry. Check is done here

                if image_object.get("datetime") == None:

                    mod_time = time.strftime('%Y:%m:%d %H:%M:%S',
                                             time.localtime(os.path.getmtime(image_file)))

                    datetime_chunk = mod_time.split(" ")
                    date_chunk = datetime_chunk[0].split(":")
                    time_chunk = datetime_chunk[1].split(":")

                    rename_date = ""
                    rename_time = ""

                    for chunk in date_chunk:
                        rename_date += chunk
                    for chunk in time_chunk:
                        rename_time += chunk

                else:
                    # Datetime is present in EXIF
                    datetime_chunk = image_object.datetime.split(" ")

                    date_chunk = datetime_chunk[0].split(":")
                    time_chunk = datetime_chunk[1].split(":")

                    rename_date = ""
                    rename_time = ""

                    for chunk in date_chunk:
                        rename_date += chunk
                    for chunk in time_chunk:
                        rename_time += chunk

                # Now software used in creating will be checked

                if image_object.get("software") == None:
                    new_name = f"Edit_{rename_date}_{rename_time}{file_suffix}"

                else:
                    software = image_object.software
                    software = software.replace(" ", "_")
                    new_name = f"Edit_{rename_date}_{rename_time}_{software}{file_suffix}"

            else:

                # No EXIF

                mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(image_file)))

                datetime_chunk = mod_time.split(" ")

                date_chunk = datetime_chunk[0].split(":")
                time_chunk = datetime_chunk[1].split(":")

                rename_date = ""
                rename_time = ""

                for chunk in date_chunk:
                    rename_date += chunk
                for chunk in time_chunk:
                    rename_time += chunk

                new_name = f"Edit_{rename_date}_{rename_time}{file_suffix}"

        else:
            # For not JPEG or not PNG files

            print("Not valid file format")
            valid_file_check = False

        if valid_file_check:

            new_image_path = input_dir / new_name

            # This section checks for duplicates
            if new_image_path.exists():
                print("Image Existing. Renaming Same Images")
                while True:
                    same_image_count += 1
                    name_split_tuple = os.path.splitext(new_name)

                    same_new_name = f"{name_split_tuple[0]}_{same_image_count}{name_split_tuple[1]}"
                    same_path = input_dir / same_new_name
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
    project_dir = script_path.parent

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

    preliminary_name(input_dir)
    proper_rename(input_dir)


if __name__ == "__main__":
    main()
