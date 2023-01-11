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
schema_display_name = "My Test Schema"
property_name = (
    "stock_symbol"  # Must be unique within a document schema (case insensitive)
)
property_display_name = "Searchable text"
property_is_searchable = True
document_display_name = "My Test Document"
document_plain_text = "This is a sample of a document's text. A plane flew over the plains of Spain avoiding the rain."
document_property_value = "GOOG"


def test_quickstart(capsys):
    project_number = get_project_number(project_id)
    quickstart_sample.quickstart(
        project_number=project_number,
        location=location,
        schema_display_name=schema_display_name,
        property_name=property_name,
        property_display_name=property_display_name,
        property_is_searchable=property_is_searchable,
        document_display_name=document_display_name,
        document_plain_text=document_plain_text,
        document_property_value=document_property_value,
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
