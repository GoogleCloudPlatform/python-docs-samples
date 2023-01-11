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

from contentwarehouse.snippets import search_documents_sample

from google.cloud import contentwarehouse
from google.cloud import resourcemanager

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"  # Format is 'us' or 'eu'
document_query_text = "document"
file_type = contentwarehouse.FileTypeFilter.FileType.DOCUMENT
histogram_query_text = 'count("DocumentSchemaId")'


def test_search_documents(capsys):
    project_number = get_project_number(project_id)
    search_documents_sample.search_documents_sample(
        project_number=project_number,
        location=location,
        document_query_text=document_query_text,
        file_type=file_type,
        histogram_query_text=histogram_query_text,
    )
    out, _ = capsys.readouterr()

    assert "document" in out


def get_project_number(project_id: str) -> str:
    client = resourcemanager.ProjectsClient()
    name = client.project_path(project=project_id)
    project = client.get_project(name=name)
    project_number = client.parse_project_path(project.name)["project"]
    return project_number
