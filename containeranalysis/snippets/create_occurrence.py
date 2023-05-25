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

# [START containeranalysis_create_occurrence]
from google.cloud.devtools import containeranalysis_v1
from grafeas.grafeas_v1 import types, Version


def create_occurrence(
    resource_url: str, note_id: str, occurrence_project: str, note_project: str
) -> types.grafeas.Occurrence:
    """Creates and returns a new occurrence of a previously
    created vulnerability note."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # note_id = 'my-note'
    # occurrence_project = 'my-gcp-project'
    # note_project = 'my-gcp-project'

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    formatted_note = f"projects/{note_project}/notes/{note_id}"
    formatted_project = f"projects/{occurrence_project}"

    occurrence = {
        "note_name": formatted_note,
        "resource_uri": resource_url,
        "vulnerability": {
            "package_issue": [
                {
                    "affected_cpe_uri": "your-uri-here",
                    "affected_package": "your-package-here",
                    "affected_version": {"kind": Version.VersionKind.MINIMUM},
                    "fixed_version": {"kind": Version.VersionKind.MAXIMUM},
                }
            ]
        },
    }

    return grafeas_client.create_occurrence(
        parent=formatted_project, occurrence=occurrence
    )


# [END containeranalysis_create_occurrence]
