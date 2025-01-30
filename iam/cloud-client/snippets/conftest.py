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

from google.api_core.exceptions import PermissionDenied
import google.auth
from google.cloud import iam_v2
from google.cloud.iam_admin_v1 import IAMClient, ListRolesRequest
from google.cloud.iam_v2 import types
import pytest

from snippets.create_deny_policy import create_deny_policy
from snippets.create_role import create_role
from snippets.delete_deny_policy import delete_deny_policy
from snippets.delete_role import delete_role
from snippets.edit_role import edit_role
from snippets.get_role import get_role

PROJECT = google.auth.default()[1]
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("IAM_CREDENTIALS", "")


@pytest.fixture
def deny_policy(capsys: "pytest.CaptureFixture[str]") -> None:
    policy_id = f"test-deny-policy-{uuid.uuid4()}"
    try:
        # Delete any existing policies. Otherwise it might throw quota issue.
        delete_existing_deny_policies(PROJECT, "test-deny-policy")

        # Create the Deny policy.
        create_deny_policy(PROJECT, policy_id)
    except PermissionDenied:
        pytest.skip("Don't have permissions to run this test.")

    yield policy_id

    # Delete the Deny policy and assert if deleted.
    delete_deny_policy(PROJECT, policy_id)
    out, _ = capsys.readouterr()
    assert re.search(f"Deleted the deny policy: {policy_id}", out)


def delete_existing_deny_policies(project_id: str, delete_name_prefix: str) -> None:
    policies_client = iam_v2.PoliciesClient()

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{PROJECT}"

    request = types.ListPoliciesRequest()
    request.parent = f"policies/{attachment_point}/denypolicies"
    for policy in policies_client.list_policies(request=request):
        if delete_name_prefix in policy.name:
            delete_deny_policy(project_id, str(policy.name).rsplit("/", 1)[-1])


@pytest.fixture(scope="session")
def iam_role() -> str:
    if PROJECT == "python-docs-samples-tests":
        # This "if" was added intentionally to prevent overflowing project with roles.
        # The limit for project is 300 custom roles and they can't be permanently deleted
        # immediately. They persist as tombstones ~7 days after deletion.
        role_id = "pythonTestCustomRole"
        try:
            role = get_role(PROJECT, role_id)
            yield role_id
        finally:
            role.etag = b""
            new_role = edit_role(role)
            assert new_role.name == role.name
            assert new_role.stage == role.stage
        return

    role_prefix = "test_iam_role"
    role_id = f"{role_prefix}_{uuid.uuid4().hex[:10]}"
    permissions = ["iam.roles.get", "iam.roles.list"]
    title = "test_role_title"

    # Delete any iam roles with `role_prefix` prefix. Otherwise, it might throw quota issue.
    delete_iam_roles_by_prefix(PROJECT, role_prefix)
    created = False
    try:
        # Create the iam role.
        create_role(PROJECT, role_id, permissions, title)
        created = True
        yield role_id
    finally:
        # Delete the iam role and assert if deleted.
        if created:
            role = delete_role(PROJECT, role_id)
            assert role.deleted


def delete_iam_roles_by_prefix(iam_role: str, delete_name_prefix: str) -> None:
    """Helper function to clean-up roles starting with a prefix.

    Args:
        iam_role: project id
        delete_name_prefix: start of the role id to be deleted.
        F.e. "test-role" in role id "test-role-123"
    """
    client = IAMClient()
    parent = f"projects/{PROJECT}"
    request = ListRolesRequest(
        parent=parent,
        view=0,
        show_deleted=False,
    )
    roles = client.list_roles(request)
    for page in roles.pages:
        for role in page.roles:
            if delete_name_prefix in role.name:
                delete_role(iam_role, role.name.rsplit("/", 1)[-1])
