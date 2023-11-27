import json
import os
import requests

from config import ROOT, API_TOKEN

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATAVERSE_DIR = os.path.join(SCRIPT_DIR, "dataverses")
DATAVERSE_NL_SUBDIR = os.path.join(DATAVERSE_DIR, "dataversenl_subverses")


def create_dataverse(parent, json_path):
    # Read dataverse data from the JSON file
    with open(json_path, "r") as json_file:
        dataverse_data = json.load(json_file)

    # Convert the dictionary to JSON format
    json_data = json.dumps(dataverse_data)

    # Set the API endpoint for creating a dataverse
    url = f"{ROOT}/api/dataverses/{parent}"

    # Set headers for the request, including the API token
    headers = {
        "X-Dataverse-key": API_TOKEN,
        "Content-Type": "application/json"
    }

    # Make the HTTP request to create the dataverse
    response = requests.post(url, headers=headers, data=json_data)

    # Check the response status
    if response.status_code == 201:
        print("Dataverse created successfully!")
        # Parse and print the JSON response
        dataverse_info = response.json()
        print("Dataverse ID:", dataverse_info.get("data").get("id"))
    else:
        print(f"Error creating dataverse. Status code: {response.status_code}")
        print("Response content:", response.text)


def create_odissei_dataverses():
    parent_root = "root"  # Set your desired parent dataverse
    parent_dv_nl = "DV_NL"
    json_paths = ["cbs.json", "cid.json", "dans.json", "dataversenl.json",
                  "hsn.json", "liss.json"]

    for json_path in json_paths:
        full_json_path = os.path.join(DATAVERSE_DIR, json_path)
        if os.path.exists(full_json_path):
            create_dataverse(parent_root, full_json_path)
        else:
            print(f"Error: JSON file not found at {full_json_path}")

    # List of JSON paths for the second set of dataverses with parent DV_NL
    json_paths_dv_nl = [
        "avans.json", "delft.json", "fontys.json", "groningen.json",
        "hanze.json", "hr.json", "leiden.json", "maastricht.json",
        "tilburg.json", "trimbos.json", "twente.json", "umcu.json",
        "utrecht.json", "vu.json"
    ]

    for json_path in json_paths_dv_nl:
        full_json_path = os.path.join(DATAVERSE_NL_SUBDIR, json_path)
        if os.path.exists(full_json_path):
            create_dataverse(parent_dv_nl, full_json_path)
        else:
            print(f"Error: JSON file not found at {full_json_path}")


if __name__ == "__main__":
    create_odissei_dataverses()
