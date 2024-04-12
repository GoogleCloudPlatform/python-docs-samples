# Copyright 2022 Google LLC
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

import os
import re
import uuid

from google.cloud import iam_v2
from google.cloud.iam_v2 import types
import pytest
from snippets.create_deny_policy import create_deny_policy
from snippets.delete_deny_policy import delete_deny_policy

PROJECT_ID = os.environ["IAM_PROJECT_ID"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["IAM_CREDENTIALS"]


@pytest.fixture
def deny_policy(capsys: "pytest.CaptureFixture[str]") -> None:
    policy_id = f"test-deny-policy-{uuid.uuid4()}"

    # Delete any existing policies. Otherwise it might throw quota issue.
    delete_existing_deny_policies(PROJECT_ID, "test-deny-policy")

    # Create the Deny policy.
    create_deny_policy(PROJECT_ID, policy_id)

    yield policy_id

    # Delete the Deny policy and assert if deleted.
    delete_deny_policy(PROJECT_ID, policy_id)
    out, _ = capsys.readouterr()
    assert re.search(f"Deleted the deny policy: {policy_id}", out)


def delete_existing_deny_policies(project_id: str, delete_name_prefix: str) -> None:
    policies_client = iam_v2.PoliciesClient()

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = types.ListPoliciesRequest()
    request.parent = f"policies/{attachment_point}/denypolicies"
    for policy in policies_client.list_policies(request=request):
        if delete_name_prefix in policy.name:
            delete_deny_policy(PROJECT_ID, str(policy.name).rsplit("/", 1)[-1])
