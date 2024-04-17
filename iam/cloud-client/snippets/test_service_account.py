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

import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.disable_service_account import disable_service_account
from snippets.enable_service_account import enable_service_account
from snippets.list_service_accounts import list_service_accounts

PROJECT_ID = os.environ["IAM_PROJECT_ID"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["IAM_CREDENTIALS"]


@pytest.fixture(scope="function")
def service_account() -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    yield name
    email = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"
    delete_service_account(PROJECT_ID, email)


def test_create_service_account(capsys: "pytest.CaptureFixture[str]", service_account: str) -> None:
    create_service_account(PROJECT_ID, service_account)
    out, _ = capsys.readouterr()
    email = f"{service_account}@{PROJECT_ID}.iam.gserviceaccount.com"
    assert re.search(f"Created a service account: {email}", out)


def test_list_service_accounts(capsys: "pytest.CaptureFixture[str]", service_account: str) -> None:
    create_service_account(PROJECT_ID, service_account)

    list_service_accounts(PROJECT_ID)
    out, _ = capsys.readouterr()
    email = f"{service_account}@{PROJECT_ID}.iam.gserviceaccount.com"
    assert re.search(f"Got service account: {email}", out)


def test_delete_service_account(capsys: "pytest.CaptureFixture[str]") -> None:
    name = f"test-{uuid.uuid4().hex[:25]}"
    create_service_account(PROJECT_ID, name)

    email = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"
    delete_service_account(PROJECT_ID, email)
    out, _ = capsys.readouterr()
    assert re.search(f"Deleted a service account: {email}", out)


def test_disable_service_account(capsys: "pytest.CaptureFixture[str]", service_account: str) -> None:
    create_service_account(PROJECT_ID, service_account)

    email = f"{service_account}@{PROJECT_ID}.iam.gserviceaccount.com"
    disable_service_account(PROJECT_ID, email)
    out, _ = capsys.readouterr()

    assert re.search(f"Disabled service account: {email}", out)


def test_enable_service_account(capsys: "pytest.CaptureFixture[str]", service_account: str) -> None:
    create_service_account(PROJECT_ID, service_account)

    email = f"{service_account}@{PROJECT_ID}.iam.gserviceaccount.com"
    disable_service_account(PROJECT_ID, email)
    out, _ = capsys.readouterr()
    assert re.search(f"Disabled service account: {email}", out)

    enable_service_account(PROJECT_ID, email)
    out, _ = capsys.readouterr()
    assert re.search(f"Enabled service account: {email}", out)
