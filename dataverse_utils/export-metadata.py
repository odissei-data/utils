import json

from pyDataverse.api import NativeApi
import requests

import config


def extract_doi_from_dataverse(alias):
    """
    Method to extract a list of DOI's from a given dataverse
    """
    api = NativeApi(
        base_url=config.ROOT,
        api_token=config.API_TOKEN
    )
    datasets = api.get_children(parent=alias, children_types=['datasets'])
    pids = []
    for child in datasets:
        pids.append(child['pid'])
    return pids


def export_metadata_by_pid(pid, metadata_format):

    # Create the URL
    url = f"{config.ROOT}/api/datasets/export?exporter={metadata_format}&persistentId={pid}"

    # Send the HTTP GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.text)
        return response.text
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def upload_exported_metadata(data):
    url = 'https://fuseki.staging.odissei.nl/odissei/data'
    headers = {"Content-Type": "application/ld+json; charset=utf-8"}  # Specify UTF-8 charset

    # Encode the data as UTF-8
    encoded_data = data.encode('utf-8')
    resp = requests.post(url, data=encoded_data, auth=('admin', 'admin'),
                         headers=headers)
    # Check if the upload was successful
    if resp.status_code == 200:
        print("Data uploaded successfully.")
    else:
        print(f"Upload failed with status code {resp.status_code}.")
        print(resp.text)  # Print any error messages returned by Fuseki


# List of Persistent Identifiers (PIDs) you want to export
pids_to_export = extract_doi_from_dataverse('cbs')
# List to store the exported metadata
metadata_list = []
metadata_format = 'OAI_ORE'
result = []
print(pids_to_export)
with open('cbs_dois.json') as f:
    parsed_json = json.load(f)
for pid in parsed_json:
    if pid not in pids_to_export:
        result.append(pid)
# # Iterate through PIDs and export metadata
# for pid in pids_to_export:
#     metadata = export_metadata_by_pid(pid, metadata_format)
#     print(metadata)
#     if metadata is not None:
#         upload_exported_metadata(metadata)
