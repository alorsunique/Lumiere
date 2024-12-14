import os
from pathlib import Path

resources_dir_text = "Resources_Path.txt"

# Creates Resources_Path.txt
with open(resources_dir_text, 'a') as writer:
    pass

# Reads Resources_Path.txt
with open("Resources_Path.txt", "r") as read_text:
    lines = read_text.readlines()

if lines:
    resources_dir = Path(lines[0].replace('"', ''))
    print(f"Resources Directory: {resources_dir}")

    # Creates Resources Directory
    if not resources_dir.exists():
        os.mkdir(resources_dir)

else:
    print("No directory")
