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
import time
import uuid

import backoff
from google.api_core.exceptions import InvalidArgument, NotFound
import google.auth
from google.iam.v1 import policy_pb2
import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.disable_service_account import disable_service_account
from snippets.enable_service_account import enable_service_account
from snippets.list_service_accounts import get_service_account, list_service_accounts
from snippets.service_account_get_policy import get_service_account_iam_policy
from snippets.service_account_rename import rename_service_account
from snippets.service_account_set_policy import set_service_account_iam_policy

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")


@pytest.fixture
def service_account_email(capsys: "pytest.CaptureFixture[str]") -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    created = False

    create_service_account(PROJECT_ID, name)
    created = False
    email = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"

    # Check if the account was created correctly using exponential backoff.
    execution_finished = False
    backoff_delay_secs = 1  # Start wait with delay of 1 second
    starting_time = time.time()
    timeout_secs = 90

    while not execution_finished:
        try:
            get_service_account(PROJECT_ID, email)
            execution_finished = True
            created = True
        except (NotFound, InvalidArgument):
            # Account not created yet, retry
            pass

        # If we haven't seen the result yet, wait again.
        if not execution_finished:
            print("- Waiting for the service account to be available...")
            time.sleep(backoff_delay_secs)
            # Double the delay to provide exponential backoff.
            backoff_delay_secs *= 2

        if time.time() > starting_time + timeout_secs:
            raise TimeoutError

    yield email

    # Cleanup after running the test
    if created:
        delete_service_account(PROJECT_ID, email)
        time.sleep(10)

        try:
            get_service_account(PROJECT_ID, email)
        except google.api_core.exceptions.NotFound:
            pass
        else:
            pytest.fail(f"The {email} service account was not deleted.")


def test_list_service_accounts(service_account_email: str) -> None:
    accounts = list_service_accounts(PROJECT_ID)
    assert len(accounts) > 0

    account_found = False
    for account in accounts:
        if account.email == service_account_email:
            account_found = True
            break
    try:
        assert account_found
    except AssertionError:
        pytest.skip("Service account was removed from outside, skipping")


@backoff.on_exception(backoff.expo, AssertionError, max_tries=6)
@backoff.on_exception(backoff.expo, NotFound, max_tries=6)
def test_disable_service_account(service_account_email: str) -> None:
    account_before = get_service_account(PROJECT_ID, service_account_email)
    assert not account_before.disabled

    account_after = disable_service_account(PROJECT_ID, service_account_email)
    assert account_after.disabled


@backoff.on_exception(backoff.expo, AssertionError, max_tries=6)
def test_enable_service_account(service_account_email: str) -> None:
    account_before = disable_service_account(PROJECT_ID, service_account_email)
    assert account_before.disabled

    account_after = enable_service_account(PROJECT_ID, service_account_email)
    assert not account_after.disabled


def test_service_account_set_policy(service_account_email: str) -> None:
    policy = get_service_account_iam_policy(PROJECT_ID, service_account_email)

    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.append(f"serviceAccount:{service_account_email}")
    policy.bindings.append(test_binding)

    try:
        new_policy = set_service_account_iam_policy(PROJECT_ID, service_account_email, policy)
    except (InvalidArgument, NotFound):
        pytest.skip("Service account was removed from outside, skipping")

    binding_found = False
    for bind in new_policy.bindings:
        if bind.role == test_binding.role:
            binding_found = test_binding.members[0] in bind.members
            break
    assert binding_found
    assert new_policy.etag != policy.etag


def test_service_account_rename(service_account_email: str) -> None:
    new_name = "New Name"
    try:
        account = rename_service_account(PROJECT_ID, service_account_email, new_name)
    except (InvalidArgument, NotFound):
        pytest.skip("Service account was removed from outside, skipping")

    assert account.display_name == new_name
