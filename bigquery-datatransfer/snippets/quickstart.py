#!/usr/bin/env python

# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys


def run_quickstart(override_values={}):
    # [START bigquerydatatransfer_quickstart]
    from google.cloud import bigquery_datatransfer

    client = bigquery_datatransfer.DataTransferServiceClient()

    # TODO: Update to your project ID.
    project_id = "my-project"
    # [END bigquerydatatransfer_quickstart]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    # [START bigquerydatatransfer_quickstart]

    # Get the full path to your project.
    parent = client.common_project_path(project_id)

    print("Supported Data Sources:")

    # Iterate over all possible data sources.
    for data_source in client.list_data_sources(parent=parent):
        print("{}:".format(data_source.display_name))
        print("\tID: {}".format(data_source.data_source_id))
        print("\tFull path: {}".format(data_source.name))
        print("\tDescription: {}".format(data_source.description))
    # [END bigquerydatatransfer_quickstart]


if __name__ == "__main__":
    run_quickstart(override_values={"project_id": sys.argv[1]})
