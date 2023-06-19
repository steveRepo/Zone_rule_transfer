# A Fresh zone is required to copy between zones. This script pulls down the all rulesets into an output folder, divded into source and target folders, with files for each rule. 
# The rule should be ready to add to an API call.

# Add your Auth
# To use: python rules.py 


import subprocess
import json
import os
import requests

AUTH_KEY = "<>"
AUTH_EMAIL = "<>"

def fetch_rulesets(zone_id, output_folder):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "X-Auth-Key": f"{AUTH_KEY}", "X-Auth-Email": f"{AUTH_EMAIL}"}
    )

    if response.status_code != 200:
        print(f"Error retrieving rulesets. Status code: {response.status_code}")
        print(response.content)
        exit(1)

    rulesets = response.json()["result"]
    print(f"Retrieved rulesets for zone {zone_id}:")
    print(rulesets)

    for ruleset in rulesets:
        ruleset_id = ruleset["id"]
        ruleset_name = ruleset["name"]
        ruleset_phase = ruleset["phase"]

        ruleset_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}"
        response = requests.get(
            ruleset_url,
            headers={"Content-Type": "application/json", "X-Auth-Key": f"{AUTH_KEY}", "X-Auth-Email": f"{AUTH_EMAIL}"}
        )

        if response.status_code != 200:
            print(f"Error retrieving ruleset details. Status code: {response.status_code}")
            print(response.content)
            exit(1)

        ruleset_details = response.json()["result"]

        if "version" in ruleset_details:
            del ruleset_details["version"]
        if "last_updated" in ruleset_details:
            del ruleset_details["last_updated"]
        if "rules" in ruleset_details:
            for rule in ruleset_details["rules"]:
                if "id" in rule:
                    del rule["id"]

        filename = f"{ruleset_phase}_{ruleset_name}.json"
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w") as json_file:
            json.dump(ruleset_details, json_file)

source_zone = input("Enter the source zone ID: ")
target_zone = input("Enter the target zone ID: ")

output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

source_folder = os.path.join(output_folder, "source")
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

target_folder = os.path.join(output_folder, "target")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

fetch_rulesets(source_zone, source_folder)
fetch_rulesets(target_zone, target_folder)

print("Complete")
