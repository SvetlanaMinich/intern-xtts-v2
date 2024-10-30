import os

cache_dir = os.path.expanduser("xtts-v2")
for root, dirs, files in os.walk(cache_dir):
    for file in files:
        if "xtts" in file.lower():  # Adjust this filter based on your model's naming
            print(os.path.join(root, file))