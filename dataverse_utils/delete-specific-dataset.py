import argparse
from pyDataverse.api import NativeApi

from config import ROOT, API_TOKEN


def delete_dataset(pid):
    api = NativeApi(ROOT, API_TOKEN)
    api.destroy_dataset(pid)


parser = argparse.ArgumentParser(
    description="Remove a specific dataset")
parser.add_argument('--pid', type=str, dest='pid',
                    help='The pid of the dataset')
args = parser.parse_args()

delete_dataset(args.pid)
