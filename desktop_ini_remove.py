# Removes desktop.ini in input folder

import os
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent

# Change working directory to project directory
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as read_text:
    lines = read_text.readlines()

resources_dir = Path(lines[0].replace('"', ''))

input_dir = resources_dir / "Input"
desktop_ini_path = input_dir / "desktop.ini"

if desktop_ini_path.exists():
    print("True")
    os.remove(desktop_ini_path)
else:
    print("False")
