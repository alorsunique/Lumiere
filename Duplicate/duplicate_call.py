# Call this script to check for duplicates

import os
import shutil
import sys
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent

# Change working directory to project directory
os.chdir(project_dir)
sys.path.append(str(project_dir))

from Duplicate import resize_recolor, first_compare, second_compare, duplicate_delete

resize_recolor.main()
first_compare.main()
second_compare.main()
duplicate_delete.main()

with open("Resources_Path.txt", "r") as read_text:
    lines = read_text.readlines()

resources_dir = Path(lines[0].replace('"', ''))

create_dir = resources_dir / "Create"
shutil.rmtree(create_dir)

json_comparison_path = resources_dir / "Comparison.json"
true_json_comparison_path = resources_dir / "True Comparison.json"

if json_comparison_path.exists():
    os.remove(json_comparison_path)
if true_json_comparison_path.exists():
    os.remove(true_json_comparison_path)
