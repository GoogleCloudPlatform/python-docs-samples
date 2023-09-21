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

from contentwarehouse.snippets import delete_folder_document_link_sample
import pytest

document_folder_link_name = "YOUR_DOCUMENT_LINK_NAME" # The name of the document-link to be deleted Format: projects/{project_number}/locations/{location}/documents/{source_document_id}/documentLinks/{document_link_id}
document_name = "YOUR_DOCUMENT_NAME" # The name of the document to be deleted Format: projects/{project_number}/locations/{location}/documents/{target_document_id
user_id = "user:xxxx@example.com" # Format is "user:xxxx@example.com"

def test_delete_folder_document_link(capsys: pytest.CaptureFixture) -> None:
    delete_folder_document_link_sample.delete_folder_document_link(
        document_folder_link_name=document_folder_link_name,
        document_name=document_name,
        user_id=user_id,
    )
    out, _ = capsys.readouterr()

    assert "Document Link to Folder Deleted Successfully" in out
