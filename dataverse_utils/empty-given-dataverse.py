import argparse
from typing import List

from pyDataverse.api import NativeApi
from pyDataverse.utils import dataverse_tree_walker

from config import API_TOKEN, ROOT


def remove_testdata(
    parent: str,
    data_types: List[str] = ["dataverses", "datasets"],
    parent_data_type: str = "dataverse",
    remove_parent: bool = False,
) -> None:
    """Remove testdata.
    Removes all data.
    It recursively collects all Dataverses and Datasets
    from a passed Dataverse down.
    """
    api = NativeApi(ROOT, API_TOKEN)

    # Clean up
    # data_types = ["dataverses", "datasets"]
    data = api.get_children(
        parent, parent_type=parent_data_type, children_types=data_types
    )
    dataverses, datasets, datafiles, = dataverse_tree_walker(data)
    dataverses.reverse()
    if parent_data_type == "dataverse" and remove_parent:
        dataverses.append({"dataverse_alias": parent})
    for ds in datasets:
        api.destroy_dataset(ds["pid"])
    for dv in dataverses:
        api.delete_dataverse(dv["dataverse_alias"])


parser = argparse.ArgumentParser(
    description="Remove all dataverses and datasets from a dataverse")
parser.add_argument('--dataverse', type=str, dest='dataverse',
                    help='The dataverse alias')
args = parser.parse_args()

remove_testdata(args.dataverse)
