# # Copyright 2023 Google LLC
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
#

import os

from contentwarehouse.snippets import quickstart_sample

from google.cloud import resourcemanager

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"  # Format is 'us' or 'eu'


def test_quickstart(capsys):
    project_number = get_project_number(project_id)
    quickstart_sample.quickstart(
        project_number=project_number,
        location=location,
    )
    out, _ = capsys.readouterr()

    assert "Rule Engine Output" in out
    assert "Document Created" in out


def get_project_number(project_id: str) -> str:
    client = resourcemanager.ProjectsClient()
    name = client.project_path(project=project_id)
    project = client.get_project(name=name)
    project_number = client.parse_project_path(project.name)["project"]
    return project_number
