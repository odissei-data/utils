import requests
from xml.etree import ElementTree


def count_datasets(oai_endpoint, oai_set=None):
    total_datasets = 0
    cursor = 0

    while True:
        # Define the OAI-PMH parameters
        params = {
            'verb': 'ListRecords',
            'metadataPrefix': 'oai_dc',
            'set': oai_set,
            'resumptionToken': cursor
        }

        # Make the request to the OAI-PMH endpoint
        response = requests.get(oai_endpoint, params=params)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the XML response
            root = ElementTree.fromstring(response.content)

            # Extract the number of records from the response
            records = root.findall('.//oai:record', namespaces={
                'oai': 'http://www.openarchives.org/OAI/2.0/'})
            total_datasets += len(records)

            # Check for the presence of a resumption token
            resumption_token = root.find('.//oai:resumptionToken', namespaces={
                'oai': 'http://www.openarchives.org/OAI/2.0/'})
            if resumption_token is not None:
                cursor = resumption_token.text
            else:
                break  # No more records
        else:
            # If the request was not successful, print the error message
            print(f"Error: {response.status_code} - {response.text}")
            return None

    return total_datasets


# Example usage:
oai_endpoint = 'https://www.oai-pmh.centerdata.nl/lissdata/oai2.php'
oai_set = None
total_datasets = count_datasets(oai_endpoint)
if total_datasets is not None:
    print(
        f"Total datasets{' in set ' + oai_set if oai_set else ''}: {total_datasets}")
