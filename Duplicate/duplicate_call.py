# Call this script to check for duplicates

import os
import shutil
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


if __name__ == "__main__":

    config_file_name = 'Lumiere_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])

    from Duplicate import resize_recolor, first_compare, second_compare, duplicate_delete

    resize_recolor.main()
    first_compare.main()
    second_compare.main()
    duplicate_delete.main()

    # Cleanup
    create_dir = resources_dir / "Create"
    shutil.rmtree(create_dir)

    json_comparison_path = resources_dir / "Comparison.json"
    true_json_comparison_path = resources_dir / "True Comparison.json"

    if json_comparison_path.exists():
        os.remove(json_comparison_path)
    if true_json_comparison_path.exists():
        os.remove(true_json_comparison_path)
