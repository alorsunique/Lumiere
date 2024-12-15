# Just call this script to run both renamer and sort

import os
import sys
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent

# Change working directory to project directory
os.chdir(project_dir)
sys.path.append(str(project_dir))

from Camera import camera_rename
from Camera import camera_sort

camera_rename.main()
camera_sort.main()
