# This script should just compare images in the Comparison folder
# Can be useful to find small differences between two similar looking images

import os
import sys
from pathlib import Path

import cv2

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent

# Change working directory to project directory
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as read_text:
    lines = read_text.readlines()

resources_dir = Path(lines[0].replace('"', ''))
comparison_dir = resources_dir / "Comparison"

if not comparison_dir.exists():
    os.mkdir(comparison_dir)

count = 0

comparison_content_list = []

for file in comparison_dir.iterdir():
    comparison_content_list.append(file.name)

for image_file in comparison_content_list:

    count += 1

    print(f"{count} | {image_file}")

    source_file = comparison_dir / image_file
    source_image = cv2.imread(str(source_file))

    source_shape = source_image.shape

    for compare_image_file in comparison_content_list[count:]:

        compare_file = comparison_dir / compare_image_file
        compare_image = cv2.imread(str(compare_file))

        if source_shape == compare_image.shape:

            print(f"Source: {image_file} | Compare: {compare_image_file}")

            difference_image = cv2.absdiff(source_image, compare_image)

            rescale_width = int(source_shape[1] / 2)
            rescale_height = int(source_shape[0] / 2)

            difference_image = cv2.resize(difference_image, (rescale_width, rescale_height))

            b_channel, g_channel, r_channel = cv2.split(difference_image)

            if cv2.countNonZero(b_channel) == 0 and cv2.countNonZero(g_channel) == 0 and cv2.countNonZero(
                    r_channel) == 0:
                print(f"Source: {image_file} | Compare: {compare_image_file} | Same Image")

            cv2.imshow(f"Difference", difference_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
