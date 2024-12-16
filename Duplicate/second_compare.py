# This script should check the potential similar images on a pixel per pixel manner

import json
import os
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

    # Reads the first comparison results
    json_comparison_path = resources_dir / "Comparison.json"
    json_file = open(json_comparison_path, "r")
    compare_pair = json.load(json_file)
    json_file.close()

    count = 0
    length_compare_pair = len(compare_pair)

    # List that stores actual similar images
    positive_pairs = []

    for pair in compare_pair:

        count += 1

        print(f"Comparison Number: {count}/{length_compare_pair} | {pair}")

        source_file = input_dir / pair[0]
        compare_file = input_dir / pair[1]

        source_image = cv2.imread(str(source_file))
        compare_image = cv2.imread(str(compare_file))

        # Check if the two images have the same dimension
        if source_image.shape == compare_image.shape:

            difference_image = cv2.subtract(source_image, compare_image)
            b_channel, g_channel, r_channel = cv2.split(difference_image)

            # Check if the two images have the exact same RGB channels
            if cv2.countNonZero(b_channel) == 0 and cv2.countNonZero(g_channel) == 0 and cv2.countNonZero(
                    r_channel) == 0:
                positive_pairs.append(pair)

    print(f"Similar Pairs: {len(positive_pairs)}")

    # JSON for true comparison

    true_json_comparison_path = resources_dir / "True Comparison.json"

    if true_json_comparison_path.exists():
        os.remove(true_json_comparison_path)

    json_file = open(true_json_comparison_path, "w")
    json.dump(positive_pairs, json_file)
    json_file.close()


if __name__ == "__main__":
    main()
