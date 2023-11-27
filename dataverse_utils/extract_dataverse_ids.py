import requests

from config import API_TOKEN, ROOT


def extract_dataverse_ids(dataverse_url, persistent_id, api_token):
    api_endpoint = f"{dataverse_url}/api/dataverses/{persistent_id}/contents"
    print(api_endpoint)
    headers = {"X-Dataverse-key": api_token,
               'Content-Type': 'application/json'}

    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        datasets = response.json()
        doi_list = [reformat_doi(dataset['persistentUrl'])
                    for dataset in datasets["data"]
                    if 'persistentUrl' in dataset
                    and 'publicationDate' not in dataset]
        print(doi_list)
        print(len(doi_list))
        return doi_list
    else:
        print(f"Request failed with status code: {response.status_code}")


def reformat_doi(unstructured_doi):
    doi = 'doi:' + unstructured_doi.split("/", 3)[3]
    return doi


if __name__ == '__main__':
    extract_dataverse_ids(ROOT, 'fill in your subverse alias here',
                          API_TOKEN)
