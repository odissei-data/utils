# Requires pyDataverse 0.3.1
import argparse

from pyDataverse.api import NativeApi
from pyDataverse.utils import dataverse_tree_walker


parser = argparse.ArgumentParser(description="Publish all datasets inside a given dataverse")
parser.add_argument('--dataverse', type=str, dest='dataverse_url', help='The dataverse url, FQDN format')
parser.add_argument('--token', type=str, dest='dataverse_token', help='The dataverse API token')
parser.add_argument('--dataverse_parent', type=str, dest='dataverse_parent', help='The Dataverse identifier')
args = parser.parse_args()
api = NativeApi(base_url=args.dataverse_url, api_token=args.dataverse_token)
children = api.get_children(parent=args.dataverse_parent, children_types=['datasets'])
pids = []
for child in children:
    pids.append(child['pid'])
    print("Pids identified: ", pids)
    print("Amount of pids: ", len(pids))
    for pid in pids:
        data = api.get_dataset(pid)
        resp = api.publish_dataset(pid=pid, release_type="major")
        print(resp.json())  
