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

from contentwarehouse.snippets import set_acl_sample
from contentwarehouse.snippets import test_utilities

from google.api_core.exceptions import InvalidArgument

import pytest

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"
document_id = "2bq3m8uih3j78"
user_id = "user:xxxx@example.com"
policy = {
    "bindings": [
        {
            "role": "roles/contentwarehouse.documentAdmin",
            "members": ["xxxx@example.com"],
        }
    ]
}


@pytest.mark.skip(
    "Document AI Warehouse is deprecated and will no longer be available on Google Cloud after January 16, 2025."
)
def test_set_project_acl(capsys: pytest.CaptureFixture) -> None:
    project_number = test_utilities.get_project_number(project_id)
    # TODO(https://github.com/GoogleCloudPlatform/python-docs-samples/issues/9821)
    # Update when test project issue is resolved.
    with pytest.raises(InvalidArgument):
        set_acl_sample.set_acl(
            project_number=project_number,
            location=location,
            policy=policy,
            user_id=user_id,
        )
        # Print error information
        capsys.readouterr()


@pytest.mark.skip(
    "Document AI Warehouse is deprecated and will no longer be available on Google Cloud after January 16, 2025."
)
def test_set_document_acl(capsys: pytest.CaptureFixture) -> None:
    project_number = test_utilities.get_project_number(project_id)
    # TODO(https://github.com/GoogleCloudPlatform/python-docs-samples/issues/9821)
    # Update when test project issue is resolved.
    with pytest.raises(InvalidArgument):
        set_acl_sample.set_acl(
            project_number=project_number,
            location=location,
            policy=policy,
            user_id=user_id,
            document_id=document_id,
        )
        # Print error information
        capsys.readouterr()
