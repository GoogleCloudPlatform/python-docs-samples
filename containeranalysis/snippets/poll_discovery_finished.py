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

# [START containeranalysis_poll_discovery_occurrence_finished]
import time

from google.cloud.devtools import containeranalysis_v1
from grafeas.grafeas_v1 import DiscoveryOccurrence


def poll_discovery_finished(
    resource_url: str, timeout_seconds: int, project_id: str
) -> None:
    """Returns the discovery occurrence for a resource once it reaches a
    terminal state."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # timeout_seconds = 20
    # project_id = 'my-gcp-project'

    deadline = time.time() + timeout_seconds

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"

    discovery_occurrence = None
    while discovery_occurrence is None:
        time.sleep(1)
        filter_str = 'resourceUrl="{}" \
                      AND noteProjectId="goog-analysis" \
                      AND noteId="PACKAGE_VULNERABILITY"'.format(
            resource_url
        )
        # [END containeranalysis_poll_discovery_occurrence_finished]
        # The above filter isn't testable, since it looks for occurrences in a
        # locked down project fall back to a more permissive filter for testing
        filter_str = 'kind="DISCOVERY" AND resourceUrl="{}"'.format(resource_url)
        # [START containeranalysis_poll_discovery_occurrence_finished]
        result = grafeas_client.list_occurrences(parent=project_name, filter=filter_str)
        # only one occurrence should ever be returned by ListOccurrences
        # and the given filter
        for item in result:
            discovery_occurrence = item
        if time.time() > deadline:
            raise RuntimeError("timeout while retrieving discovery occurrence")

    status = DiscoveryOccurrence.AnalysisStatus.PENDING
    while (
        status != DiscoveryOccurrence.AnalysisStatus.FINISHED_UNSUPPORTED
        and status != DiscoveryOccurrence.AnalysisStatus.FINISHED_FAILED
        and status != DiscoveryOccurrence.AnalysisStatus.FINISHED_SUCCESS
    ):
        time.sleep(1)
        updated = grafeas_client.get_occurrence(name=discovery_occurrence.name)
        status = updated.discovery.analysis_status
        if time.time() > deadline:
            raise RuntimeError("timeout while waiting for terminal state")
    return discovery_occurrence


# [END containeranalysis_poll_discovery_occurrence_finished]
