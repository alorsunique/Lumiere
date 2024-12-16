# This script should downscale the image and convert it to grayscale for faster filtering

import os
import shutil
import sys
from pathlib import Path

import cv2


def main():
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
