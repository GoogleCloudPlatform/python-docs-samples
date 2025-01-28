# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re

import backoff
from google.api_core.exceptions import Aborted, InvalidArgument
from google.cloud.iam_admin_v1 import GetRoleRequest, IAMClient, ListRolesRequest, Role
import pytest

from snippets.delete_role import delete_role, undelete_role
from snippets.disable_role import disable_role
from snippets.edit_role import edit_role
from snippets.get_role import get_role
from snippets.list_roles import list_roles

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")


def test_retrieve_role(iam_role: str) -> None:
    # Test role retrieval, given the iam role id.
    get_role(PROJECT_ID, iam_role)
    client = IAMClient()
    parent = f"projects/{PROJECT_ID}"
    request = ListRolesRequest(parent=parent, show_deleted=False)
    roles = client.list_roles(request)
    found = False
    for page in roles.pages:
        for role in page.roles:
            if iam_role in role.name:
                found = True
                break
        if found:
            break

    assert found, f"Role {iam_role} was not found in the list of roles."


def test_delete_undelete_role(iam_role: str) -> None:
    client = IAMClient()
    name = f"projects/{PROJECT_ID}/roles/{iam_role}"
    request = GetRoleRequest(name=name)

    delete_role(PROJECT_ID, iam_role)
    deleted_role = client.get_role(request)
    assert deleted_role.deleted

    undelete_role(PROJECT_ID, iam_role)
    undeleted_role = client.get_role(request)
    assert not undeleted_role.deleted


def test_list_roles(capsys: "pytest.CaptureFixture[str]", iam_role: str) -> None:
    # Test role list retrieval, given the iam role id should be listed.
    list_roles(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert re.search(iam_role, out)


@backoff.on_exception(backoff.expo, Aborted, max_tries=3)
def test_edit_role(iam_role: str) -> None:
    client = IAMClient()
    name = f"projects/{PROJECT_ID}/roles/{iam_role}"
    request = GetRoleRequest(name=name)
    role = client.get_role(request)
    title = "updated role title"
    role.title = title
    edit_role(role)
    updated_role = client.get_role(request)
    assert updated_role.title == title


@backoff.on_exception(backoff.expo, Aborted, max_tries=5)
@backoff.on_exception(backoff.expo, InvalidArgument, max_tries=5)
def test_disable_role(capsys: "pytest.CaptureFixture[str]", iam_role: str) -> None:
    disable_role(PROJECT_ID, iam_role)
    client = IAMClient()
    name = f"projects/{PROJECT_ID}/roles/{iam_role}"
    request = GetRoleRequest(name=name)
    role = client.get_role(request)
    assert role.stage == Role.RoleLaunchStage.DISABLED
