# This script should fix the PNG edits that were converted to JPG
# A proper EXIF and proper time tag will be added to the files
# Use for edits with the format Edit_{date}_{time}_ConvertedPNG

# This script should not be used anymore as all ConvertedPNG images are processed already


import os
import sys
import time
from datetime import datetime
from pathlib import Path

from exif import Image

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent

# Change working directory to project directory
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as read_text:
    lines = read_text.readlines()

resources_dir = Path(lines[0].replace('"', ''))

input_dir = resources_dir / "Input"
create_dir = resources_dir / "Create"

if not create_dir.exists():
    os.mkdir(create_dir)

for image_file in input_dir.iterdir():
    print(image_file.name)

    opened_file = open(image_file, 'rb')
    image_object = Image(opened_file)
    opened_file.close()

    # In this part of the script, the date and time are extracted

    filename_split = image_file.stem.split("_")

    date_chunk = filename_split[1]
    time_chunk = filename_split[2]

    date_chunk = f"{date_chunk[:4]}:{date_chunk[4:6]}:{date_chunk[6:]}"
    time_chunk = f"{time_chunk[:2]}:{time_chunk[2:4]}:{time_chunk[4:]}"

    datetime_info = f"{date_chunk} {time_chunk}"
    datetime_object = datetime.strptime(datetime_info, '%Y:%m:%d %H:%M:%S')

    print(f"Date Time Info: {datetime_info} | Date Time Object: {datetime_object}")

    creation_time = time.mktime(datetime_object.timetuple())
    modification_time = time.mktime(datetime_object.timetuple())

    image_object["software"] = "Converted PNG"
    image_object["datetime_original"] = datetime_info
    image_object["datetime"] = datetime_info

    print(f"EXIF: {image_object.has_exif} | EXIF List: {image_object.list_all()}")

    create_image_path = create_dir / f"New_{image_file.name}"

    opened_create = open(create_image_path, 'wb')
    opened_create.write(image_object.get_file())
    opened_create.close()

    os.utime(create_image_path, (creation_time, modification_time))
