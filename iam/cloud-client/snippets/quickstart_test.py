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

import re
import uuid

import backoff
from google.api_core.exceptions import Aborted
import google.auth
import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.quickstart import quickstart


PROJECT = google.auth.default()[1]


@pytest.fixture
def test_member(capsys: "pytest.CaptureFixture[str]") -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    created = False
    try:
        create_service_account(PROJECT, name)
        created = True
        email = f"{name}@{PROJECT}.iam.gserviceaccount.com"
        member = f"serviceAccount:{email}"
        yield member
    finally:
        if created:
            delete_service_account(PROJECT, email)
            out, _ = capsys.readouterr()
            assert re.search(f"Deleted a service account: {email}", out)


def test_quickstart(test_member: str, capsys: pytest.CaptureFixture) -> None:
    @backoff.on_exception(backoff.expo, Aborted, max_tries=6)
    def test_call() -> None:
        quickstart(PROJECT, test_member)
        out, _ = capsys.readouterr()
        assert test_member in out

    test_call()
