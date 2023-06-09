#!/bin/python
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START containeranalysis_discovery_info]
from google.cloud.devtools import containeranalysis_v1


def get_discovery_info(resource_url: str, project_id: str) -> None:
    """Retrieves and prints the discovery occurrence created for a specified
    image. The discovery occurrence contains information about the initial
    scan on the image."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # project_id = 'my-gcp-project'

    filter_str = f'kind="DISCOVERY" AND resourceUrl="{resource_url}"'
    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"
    response = grafeas_client.list_occurrences(parent=project_name, filter_=filter_str)
    for occ in response:
        print(occ)


# [END containeranalysis_discovery_info]
