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
import time
import uuid

import backoff
from google.api_core.exceptions import Aborted, InvalidArgument, NotFound
import pytest

from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.list_service_accounts import get_service_account
from snippets.quickstart import quickstart

# Your Google Cloud project ID.
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")


@pytest.fixture
def test_member(capsys: "pytest.CaptureFixture[str]") -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    created = False

    create_service_account(PROJECT_ID, name)
    created = False
    email = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"
    member = f"serviceAccount:{email}"

    # Check if the account was created correctly using exponential backoff.
    execution_finished = False
    backoff_delay_secs = 1  # Start wait with delay of 1 second
    starting_time = time.time()
    timeout_secs = 90

    while not execution_finished:
        try:
            print("- Checking if the service account is available...")
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

    print("- Service account is ready to be used")
    yield member

    # Cleanup after running the test
    if created:
        delete_service_account(PROJECT_ID, email)
        out, _ = capsys.readouterr()
        assert re.search(f"Deleted a service account: {email}", out)


def test_quickstart(test_member: str, capsys: pytest.CaptureFixture) -> None:
    @backoff.on_exception(backoff.expo, Aborted, max_tries=6)
    @backoff.on_exception(backoff.expo, InvalidArgument, max_tries=6)
    def test_call() -> None:
        quickstart(PROJECT_ID, test_member)
        out, _ = capsys.readouterr()
        assert test_member in out

    test_call()
