import requests

from config import ROOT, API_TOKEN


def get_most_recent_publication_date(dataverse_url, subverse, key):
    api_endpoint = f"{dataverse_url}/api/search"
    headers = {"X-Dataverse-key": key, 'Content-Type': 'application/json'}
    params = {
        'q': '*',
        'type': 'dataset',
        'subtree': f'{subverse}',
        'sort': 'date',
        'per_page': 1
    }

    response = requests.get(api_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        search_results = response.json()
        if search_results['data']['total_count'] > 0:
            most_recent_dataset = search_results['data']['items'][0]
            most_recent_date = most_recent_dataset['published_at']
            return most_recent_date
        else:
            print("No datasets found in this subverse.")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


subverse = "cbs"

most_recent_date = get_most_recent_publication_date(ROOT, subverse, API_TOKEN)

print(f'Most recent publication date: {most_recent_date}')
