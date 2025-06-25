# This script should check the downscaled images for potential similar images

import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np
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

    create_dir = resources_dir / "Create"

    # Take note of all images in Create

    create_content_list = []

    for file in create_dir.iterdir():
        create_content_list.append(file.name)

    area = float(128 * 128)

    # Comparison threshold
    threshold = float(0.01)

    count = 0
    threshold_count = 0

    # List that holds pairs of potential similar images
    compare_pair_list = []

    for image_file in create_content_list:

        # image_file is the first image of the two being compared

        count += 1

        in_count = count

        source_file = os.path.join(create_dir, image_file)
        source_image = cv2.imread(source_file)

        for compare_image_file in create_content_list[count:]:

            # compare_image_file is the second image of the two being compared

            in_count += 1

            print(f"{count} {image_file} | {in_count} {compare_image_file}")

            compare_file = create_dir / compare_image_file
            compare_image = cv2.imread(str(compare_file))

            # Perform the comparison here

            difference_image = cv2.absdiff(source_image, compare_image)

            error = np.sum(difference_image ** 2)
            MSE = error / area
            RMSE = np.sqrt(MSE)

            if RMSE <= threshold:
                threshold_count += 1
                print(
                    f"Source: {count} {image_file} | Compare: {in_count} {compare_image_file} | RMSE: {RMSE}  | {threshold_count}")
                compare_pair_list.append([image_file, compare_image_file])

    # JSON for comparison

    json_comparison_path = resources_dir / "Comparison.json"

    if json_comparison_path.exists():
        os.remove(json_comparison_path)

    json_file = open(json_comparison_path, "w")
    json.dump(compare_pair_list, json_file)
    json_file.close()


if __name__ == "__main__":
    main()
