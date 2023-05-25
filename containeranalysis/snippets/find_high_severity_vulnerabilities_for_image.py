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

# [START containeranalysis_filter_vulnerability_occurrences]
from typing import List

from grafeas.grafeas_v1 import types


def find_high_severity_vulnerabilities_for_image(
    resource_url: str, project_id: str
) -> List[types.grafeas.Occurrence]:
    """Retrieves a list of only high vulnerability occurrences associated
    with a resource."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # project_id = 'my-gcp-project'

    from grafeas.grafeas_v1 import Severity
    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"

    filter_str = 'kind="VULNERABILITY" AND resourceUrl="{}"'.format(resource_url)
    vulnerabilities = grafeas_client.list_occurrences(
        parent=project_name, filter=filter_str
    )
    filtered_list = []
    for v in vulnerabilities:
        if (
            v.vulnerability.effective_severity == Severity.HIGH
            or v.vulnerability.effective_severity == Severity.CRITICAL
        ):
            filtered_list.append(v)
    return filtered_list


# [END containeranalysis_filter_vulnerability_occurrences]
