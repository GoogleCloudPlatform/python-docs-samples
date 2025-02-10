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

import json
import os
import time
import uuid

from google.api_core.exceptions import InvalidArgument, NotFound
import pytest
from snippets.create_key import create_key
from snippets.create_service_account import create_service_account
from snippets.delete_key import delete_key
from snippets.delete_service_account import delete_service_account
from snippets.list_keys import list_keys
from snippets.list_service_accounts import get_service_account

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")


def delete_service_account_with_backoff(email: str) -> None:
    """Check if the account was deleted correctly using exponential backoff."""

    delete_service_account(PROJECT_ID, email)

    backoff_delay_secs = 1  # Start wait with delay of 1 second
    starting_time = time.time()
    timeout_secs = 90

    while time.time() < starting_time + timeout_secs:
        try:
            get_service_account(PROJECT_ID, email)
        except (NotFound, InvalidArgument):
            # Service account deleted successfully
            return

        # In case the account still exists, wait again.
        print("- Waiting for the service account to be deleted...")
        time.sleep(backoff_delay_secs)
        # Double the delay to provide exponential backoff
        backoff_delay_secs *= 2

    pytest.fail(f"The {email} service account was not deleted.")


@pytest.fixture
def service_account(capsys: "pytest.CaptureFixture[str]") -> str:
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
            # Account not created yet, retry getting it.
            pass

        # If account is not found yet, wait again.
        if not execution_finished:
            print("- Waiting for the service account to be available...")
            time.sleep(backoff_delay_secs)
            # Double the delay to provide exponential backoff
            backoff_delay_secs *= 2

        if time.time() > starting_time + timeout_secs:
            raise TimeoutError

    yield email

    # Cleanup after running the test
    if created:
        delete_service_account_with_backoff(email)


def key_found(project_id: str, account: str, key_id: str) -> bool:
    keys = list_keys(project_id, account)
    key_found = False
    for key in keys:
        out_key_id = key.name.split("/")[-1]
        if out_key_id == key_id:
            key_found = True
            break
    return key_found


def test_delete_service_account_key(service_account: str) -> None:
    try:
        key = create_key(PROJECT_ID, service_account)
    except NotFound:
        pytest.skip("Service account was removed from outside, skipping")
    json_key_data = json.loads(key.private_key_data)
    key_id = json_key_data["private_key_id"]
    time.sleep(5)
    assert key_found(PROJECT_ID, service_account, key_id)

    delete_key(PROJECT_ID, service_account, key_id)
    time.sleep(10)
    assert not key_found(PROJECT_ID, service_account, key_id)
