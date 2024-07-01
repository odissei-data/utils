import requests

from config import ROOT, API_TOKEN

# Define your Dataverse base URL and API token


# Define the dataset identifier and the metadata you want to update
dataset_id = "your-dataset-id"
new_metadata = {
    "title": "New Title",
    "author": "New Author",
    # Add more metadata fields as needed
}

headers = {"X-Dataverse-key": API_TOKEN}

# Endpoint for updating dataset metadata
url = f"{ROOT}/api/datasets/{dataset_id}/editMetadata"

# Send a PUT request with the updated metadata
response = requests.put(url, json=new_metadata, headers=headers)

# Check the response
if response.status_code == 200:
    print("Metadata updated successfully")
else:
    print(f"Failed to update metadata: {response.status_code} - {response.text}")
