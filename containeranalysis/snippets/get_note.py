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

# [START containeranalysis_get_note]
from google.cloud.devtools import containeranalysis_v1
from grafeas.grafeas_v1 import types


def get_note(note_id: str, project_id: str) -> types.grafeas.Note:
    """Retrieves and prints a specified note from the server."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    note_name = f"projects/{project_id}/notes/{note_id}"
    response = grafeas_client.get_note(name=note_name)
    return response


# [END containeranalysis_get_note]
