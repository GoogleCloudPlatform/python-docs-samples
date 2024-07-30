# Copyright 2024 Google LLC
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

import re
from typing import Callable, Union
import uuid

import backoff
from google.api_core.exceptions import Aborted, InvalidArgument, NotFound
import google.auth
from google.iam.v1 import policy_pb2
import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.get_policy import get_project_policy
from snippets.modify_policy_add_member import modify_policy_add_member
from snippets.modify_policy_remove_member import modify_policy_remove_member
from snippets.query_testable_permissions import query_testable_permissions
from snippets.set_policy import set_project_policy

PROJECT = google.auth.default()[1]


@pytest.fixture
def service_account(capsys: "pytest.CaptureFixture[str]") -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    created = False
    try:
        create_service_account(PROJECT, name)
        created = True
        email = f"{name}@{PROJECT}.iam.gserviceaccount.com"
        yield email
    finally:
        if created:
            delete_service_account(PROJECT, email)
            out, _ = capsys.readouterr()
            assert re.search(f"Deleted a service account: {email}", out)


@pytest.fixture
def project_policy() -> policy_pb2.Policy:
    try:
        policy = get_project_policy(PROJECT)
        policy_copy = policy_pb2.Policy()
        policy_copy.CopyFrom(policy)
        yield policy_copy
    finally:
        execute_wrapped(set_project_policy, PROJECT, policy, False)


@backoff.on_exception(backoff.expo, Aborted, max_tries=6)
def execute_wrapped(
    func: Callable, *args: Union[str, policy_pb2.Policy]
) -> policy_pb2.Policy:
    try:
        return func(*args)
    except (NotFound, InvalidArgument):
        pytest.skip("Service account wasn't created")


def test_set_project_policy(project_policy: policy_pb2.Policy) -> None:
    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT}@appspot.gserviceaccount.com",
        ]
    )
    project_policy.bindings.append(test_binding)

    policy = execute_wrapped(set_project_policy, PROJECT, project_policy)

    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found


def test_modify_policy_add_member(
    project_policy: policy_pb2.Policy, service_account: str
) -> None:
    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT}@appspot.gserviceaccount.com",
        ]
    )
    project_policy.bindings.append(test_binding)

    policy = execute_wrapped(set_project_policy, PROJECT, project_policy)
    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found

    member = f"serviceAccount:{service_account}"
    policy = execute_wrapped(modify_policy_add_member, PROJECT, role, member)

    member_added = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            member_added = member in bind.members
            break
    assert member_added


def test_modify_policy_remove_member(
    project_policy: policy_pb2.Policy, service_account: str
) -> None:
    role = "roles/viewer"
    member = f"serviceAccount:{service_account}"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT}@appspot.gserviceaccount.com",
            member,
        ]
    )
    project_policy.bindings.append(test_binding)

    policy = execute_wrapped(set_project_policy, PROJECT, project_policy)

    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found

    policy = execute_wrapped(modify_policy_remove_member, PROJECT, role, member)

    member_removed = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            member_removed = member not in bind.members
            break
    assert member_removed


def test_query_testable_permissions() -> None:
    permissions = [
        "resourcemanager.projects.get",
        "resourcemanager.projects.delete",
    ]
    query_permissions = query_testable_permissions(PROJECT, permissions)

    assert permissions[0] in query_permissions
    assert permissions[1] not in query_permissions
