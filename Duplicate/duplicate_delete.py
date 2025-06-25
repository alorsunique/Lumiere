# This should delete the duplicates

import json
import os
import sys
from pathlib import Path

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

    input_dir = resources_dir / "Input"

    # Reads the second comparison results
    true_json_comparison_path = resources_dir / "True Comparison.json"
    json_file = open(true_json_comparison_path, "r")
    positive_pair_list = json.load(json_file)
    json_file.close()

    processed_pair_list = []
    processed_group_list = []

    count = 0

    for root_pair in positive_pair_list:

        count += 1

        # This checks if the current pair was processed on a previous pair
        if root_pair not in processed_pair_list:

            # If it reaches here, this means that the two images in the pair are entirely new

            processed_pair_list.append(root_pair)

            group_list = []

            # This should append the current pair to the group
            for entry in root_pair:
                group_list.append(entry)

            # It is possible that the same image would have many pairs
            # This is because multiple copies may exist
            # Comparison of those copies are also noted since there is no way to identify the true source image
            # The next for loop will check other pairs for this

            for next_pair in positive_pair_list[count:]:
                if next_pair not in processed_pair_list:

                    # Converts the group list and the current next pair into sets for easier comparison
                    first_set = set(group_list)
                    second_set = set(next_pair)

                    if len(first_set.intersection(second_set)) > 0:
                        # If it reaches here, this means that the current next pair has an entry that is in group list
                        # This means that the current next pair is also a duplicate of the images of the root pair
                        for entry in next_pair:
                            if entry not in group_list:
                                group_list.append(entry)

                        processed_pair_list.append(next_pair)

            # The group list should contain all duplicate images at this point
            # Appends the processed group list with the current group
            processed_group_list.append(group_list)

    deleted_count = 0

    for entry in processed_group_list:
        print(f"Current Group: {entry} | {len(entry)}")

        deleted_count += len(entry) - 1

        # This should delete all images present in a group except the first one
        for image_file in entry[1:]:

            image_path = input_dir / image_file

            if os.path.exists(image_path):
                os.remove(image_path)

    print(f"Deleted Count: {deleted_count}")


if __name__ == "__main__":
    main()
