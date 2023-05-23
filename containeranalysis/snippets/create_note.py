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

# [START containeranalysis_create_note]
from google.cloud.devtools import containeranalysis_v1
from grafeas.grafeas_v1 import types, Version


def create_note(note_id: str, project_id: str) -> types.grafeas.Note:
    """Creates and returns a new vulnerability note."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"
    note = {
        "vulnerability": {
            "details": [
                {
                    "affected_cpe_uri": "your-uri-here",
                    "affected_package": "your-package-here",
                    "affected_version_start": {"kind": Version.VersionKind.MINIMUM},
                    "fixed_version": {"kind": Version.VersionKind.MAXIMUM},
                }
            ]
        }
    }
    response = grafeas_client.create_note(
        parent=project_name, note_id=note_id, note=note
    )
    return response


# [END containeranalysis_create_note]
