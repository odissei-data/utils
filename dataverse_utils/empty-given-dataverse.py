import os
import sys
from json import load
from time import sleep
from typing import Dict
from typing import List

import requests
from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile
from pyDataverse.models import Dataset
from pyDataverse.models import Dataverse
from pyDataverse.utils import dataverse_tree_walker
from pyDataverse.utils import read_file
from pyDataverse.utils import read_json
from pyDataverse.utils import write_json


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
    api = NativeApi('http://portal.dev.odissei.nl', '95ece972-6e98-4239-806e-f225bb6585aa')

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    remove_testdata('cbs')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
