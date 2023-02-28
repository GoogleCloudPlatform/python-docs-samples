
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

from contentwarehouse.snippets import create_folder_link_document_sample
from contentwarehouse.snippets import test_utilities
import pytest

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"  # Format is 'us' or 'eu'
user_id = "user:xxxx@example.com" # Format is "user:xxxx@example.com"

def test_create_folder_link_document(capsys: pytest.CaptureFixture) -> None:
    project_number = test_utilities.get_project_number(project_id)
    create_folder_link_document_sample.create_folder_link_document(
        project_number=project_number,
        location=location,
        user_id=user_id,
    )
    out, _ = capsys.readouterr()

    assert "Rule Engine Output" in out
    assert "Folder Created" in out
    assert "Rule Engine Output" in out
    assert "Document Created" in out
    assert "Link Created" in out
    assert "Validate Link Created" in out