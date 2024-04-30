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
import uuid

import google.auth
from google.iam.v1 import policy_pb2
import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.disable_service_account import disable_service_account
from snippets.enable_service_account import enable_service_account
from snippets.list_service_accounts import get_service_account, list_service_accounts
from snippets.service_account_get_policy import get_policy
from snippets.service_account_rename import rename_service_account
from snippets.service_account_set_policy import set_policy

PROJECT = google.auth.default()[1]


@pytest.fixture(scope="function")
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


def test_list_service_accounts(service_account: str) -> None:
    accounts = list_service_accounts(PROJECT)
    account_found = False
    for account in accounts:
        if account.email == service_account:
            account_found = True
            break
    assert account_found


def test_disable_service_account(service_account: str) -> None:
    account_before = get_service_account(PROJECT, service_account)
    assert not account_before.disabled

    account_after = disable_service_account(PROJECT, service_account)
    assert account_after.disabled


def test_enable_service_account(service_account: str) -> None:
    account_before = disable_service_account(PROJECT, service_account)
    assert account_before.disabled

    account_after = enable_service_account(PROJECT, service_account)
    assert not account_after.disabled


def test_service_account_set_policy(service_account: str) -> None:
    policy = get_policy(PROJECT, service_account)

    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.append(f"serviceAccount:{service_account}")
    policy.bindings.append(test_binding)

    new_policy = set_policy(PROJECT, service_account, policy)

    binding_found = False
    for bind in new_policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found
    assert new_policy.etag != policy.etag


def test_service_account_rename(service_account: str) -> None:
    new_name = "New Name"
    account = rename_service_account(PROJECT, service_account, new_name)
    assert account.display_name == new_name
