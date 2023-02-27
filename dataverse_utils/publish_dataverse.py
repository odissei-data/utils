# Requires pyDataverse 0.3.1
import argparse
from pyDataverse.api import NativeApi
from extract_dataverse_ids import extract_dataverse_ids

parser = argparse.ArgumentParser(description="Publish all datasets inside a given dataverse")
parser.add_argument('--dataverse', type=str, dest='dataverse_url', help='The dataverse url, FQDN format')
parser.add_argument('--token', type=str, dest='dataverse_token', help='The dataverse API token')
parser.add_argument('--dataverse_parent', type=str, dest='dataverse_parent', help='The Dataverse identifier')
args = parser.parse_args()
api = NativeApi(base_url=args.dataverse_url, api_token=args.dataverse_token)
pids = extract_dataverse_ids(dataverse_url=args.dataverse_url,
                             persistent_id=args.dataverse_parent,
                             api_token=args.dataverse_token)

for pid in pids:
    data = api.get_dataset(pid)
    resp = api.publish_dataset(pid=pid, release_type="major")
    print(resp.json())
