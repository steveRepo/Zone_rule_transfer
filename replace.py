# A Fresh zone is required as this script only copies over the difference between the 2 zones from the previous rules.py script. 
# Add your Auth
# To use: python rules.py 

import os
import shutil
import json
import requests

AUTH_KEY = "<>"
AUTH_EMAIL = "<>"

def compare_and_copy_diff(source_folder, target_folder, diff_folder):
    source_files = set(os.listdir(source_folder))
    target_files = set(os.listdir(target_folder))

    diff_files = source_files.difference(target_files)

    if not os.path.exists(diff_folder):
        os.makedirs(diff_folder)

    for file in diff_files:
        source_file_path = os.path.join(source_folder, file)
        diff_file_path = os.path.join(diff_folder, file)
        shutil.copyfile(source_file_path, diff_file_path)

def create_rulesets_from_diff(diff_folder, target_zone_id):
    for file in os.listdir(diff_folder):
        file_path = os.path.join(diff_folder, file)

        with open(file_path, "r") as json_file:
            ruleset_data = json.load(json_file)

        if "id" in ruleset_data:
            del ruleset_data["id"]
        if "source" in ruleset_data:
            del ruleset_data["source"]

        url = f"https://api.cloudflare.com/client/v4/zones/{target_zone_id}/rulesets"

        response = requests.post(
            url,
            json=ruleset_data,
            headers={"Content-Type": "application/json", "X-Auth-Key": f"{AUTH_KEY}", "X-Auth-Email": f"{AUTH_EMAIL}"}
        )

        if response.status_code != 200:
            print(f"Error creating ruleset from file {file}. Status code: {response.status_code}")
            print(response.content)
            exit(1)

        print(f"Ruleset {file} created successfully in the target zone.")

# Prompt the user for the target zone ID
target_zone_id = input("Enter the target zone ID: ")

output_folder = "output"
source_folder = os.path.join(output_folder, "source")
target_folder = os.path.join(output_folder, "target")
diff_folder = os.path.join(output_folder, "diff")

compare_and_copy_diff(source_folder, target_folder, diff_folder)
create_rulesets_from_diff(diff_folder, target_zone_id)

print("Complete")
