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

# [START containeranalysis_occurrences_for_note]
from google.cloud.devtools import containeranalysis_v1


def get_occurrences_for_note(note_id: str, project_id: str) -> int:
    """Retrieves all the occurrences associated with a specified Note.
    Here, all occurrences are printed and counted."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    note_name = f"projects/{project_id}/notes/{note_id}"

    response = grafeas_client.list_note_occurrences(name=note_name)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count


# [END containeranalysis_occurrences_for_note]
