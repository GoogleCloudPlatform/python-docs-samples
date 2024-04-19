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

import re
import uuid

import google.auth
import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.disable_service_account import disable_service_account
from snippets.enable_service_account import enable_service_account
from snippets.list_service_accounts import get_service_account, list_service_accounts

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


def test_list_service_accounts(service_account: str) -> None:
    accounts = list_service_accounts(PROJECT)
    account_found = False
    for account in accounts:
        if account.email == service_account:
            account_found = True
            break
    assert account_found


def test_disable_service_account(service_account: str) -> None:
    disable_service_account(PROJECT, service_account)
    account = get_service_account(PROJECT, service_account)
    assert account.disabled


def test_enable_service_account(service_account: str) -> None:
    disable_service_account(PROJECT, service_account)
    account = get_service_account(PROJECT, service_account)
    assert account.disabled

    enable_service_account(PROJECT, service_account)
    account = get_service_account(PROJECT, service_account)
    assert not account.disabled
