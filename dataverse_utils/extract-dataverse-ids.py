import requests

from Licenses.config import PRODUCTION_API_TOKEN, API_TOKEN, ROOT


def extract_dataverse_ids(dataverse_url, persistent_id, api_token):
    api_endpoint = f"{dataverse_url}/api/dataverses/{persistent_id}/contents"
    print(api_endpoint)
    headers = {"X-Dataverse-key": api_token,
               'Content-Type': 'application/json'}

    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        datasets = response.json()
        dois = [dataset['persistentUrl'] for dataset in datasets["data"] if
                'persistentUrl' in dataset]
        print(dois)
    else:
        print(f"Request failed with status code: {response.status_code}")


if __name__ == '__main__':
    extract_dataverse_ids(ROOT, 'easy',
                          API_TOKEN)
