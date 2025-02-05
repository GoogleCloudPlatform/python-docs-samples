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

import os
import re
import time
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
from snippets.list_service_accounts import get_service_account
from snippets.modify_policy_add_member import modify_policy_add_principal
from snippets.modify_policy_remove_member import modify_policy_remove_principal
from snippets.query_testable_permissions import query_testable_permissions
from snippets.set_policy import set_project_policy

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")


@pytest.fixture
def service_account(capsys: "pytest.CaptureFixture[str]") -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    created = False
    try:
        create_service_account(PROJECT_ID, name)
        created = True
        email = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"
        member = f"serviceAccount:{email}"

        # Check if the account was created correctly using exponential backoff.
        execution_finished = False
        backoff_delay_secs = 1  # Start wait with delay of 1 second
        starting_time = time.time()
        timeout_secs = 90

        while not execution_finished:
            try:
                get_service_account(PROJECT_ID, email)
                execution_finished = True
            except google.api_core.exceptions.NotFound:
                # Account not created yet
                pass

            # If we haven't seen the result yet, wait again.
            if not execution_finished:
                print("- Waiting for the service account to be available...")
                time.sleep(backoff_delay_secs)
                # Double the delay to provide exponential backoff.
                backoff_delay_secs *= 2

            if time.time() > starting_time + timeout_secs:
                raise TimeoutError
        yield member
    finally:
        if created:
            delete_service_account(PROJECT_ID, email)
            out, _ = capsys.readouterr()
            assert re.search(f"Deleted a service account: {email}", out)


@pytest.fixture
def project_policy() -> policy_pb2.Policy:
    try:
        policy = get_project_policy(PROJECT_ID)
        policy_copy = policy_pb2.Policy()
        policy_copy.CopyFrom(policy)
        yield policy_copy
    finally:
        execute_wrapped(set_project_policy, PROJECT_ID, policy, False)


@backoff.on_exception(backoff.expo, Aborted, max_tries=6)
def execute_wrapped(
    func: Callable, *args: Union[str, policy_pb2.Policy]
) -> policy_pb2.Policy:
    try:
        return func(*args)
    except (NotFound, InvalidArgument):
        pytest.skip("Service account wasn't created")


@backoff.on_exception(backoff.expo, Aborted, max_tries=6)
def test_set_project_policy(project_policy: policy_pb2.Policy) -> None:
    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT_ID}@appspot.gserviceaccount.com",
        ]
    )
    project_policy.bindings.append(test_binding)

    policy = execute_wrapped(set_project_policy, PROJECT_ID, project_policy)

    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found


@backoff.on_exception(backoff.expo, Aborted, max_tries=6)
def test_modify_policy_add_principal(
    project_policy: policy_pb2.Policy, service_account: str
) -> None:
    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT_ID}@appspot.gserviceaccount.com",
        ]
    )
    project_policy.bindings.append(test_binding)

    policy = execute_wrapped(set_project_policy, PROJECT_ID, project_policy)
    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found

    member = f"serviceAccount:{service_account}"
    policy = execute_wrapped(modify_policy_add_principal, PROJECT_ID, role, member)

    member_added = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            member_added = member in bind.members
            break
    assert member_added


@backoff.on_exception(backoff.expo, Aborted, max_tries=6)
def test_modify_policy_remove_member(
    project_policy: policy_pb2.Policy, service_account: str
) -> None:
    role = "roles/viewer"
    member = f"serviceAccount:{service_account}"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT_ID}@appspot.gserviceaccount.com",
            member,
        ]
    )
    project_policy.bindings.append(test_binding)

    policy = execute_wrapped(set_project_policy, PROJECT_ID, project_policy)

    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found

    policy = execute_wrapped(modify_policy_remove_principal, PROJECT_ID, role, member)

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
    query_permissions = query_testable_permissions(PROJECT_ID, permissions)

    assert permissions[0] in query_permissions
    assert permissions[1] not in query_permissions
