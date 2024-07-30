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
import re
import time
import uuid

from google.api_core.exceptions import NotFound
import google.auth
import pytest
from snippets.create_key import create_key
from snippets.create_service_account import create_service_account
from snippets.delete_key import delete_key
from snippets.delete_service_account import delete_service_account
from snippets.list_keys import list_keys

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
        key = create_key(PROJECT, service_account)
    except NotFound:
        pytest.skip("Service account was removed from outside, skipping")
    json_key_data = json.loads(key.private_key_data)
    key_id = json_key_data["private_key_id"]
    time.sleep(5)
    assert key_found(PROJECT, service_account, key_id)

    delete_key(PROJECT, service_account, key_id)
    time.sleep(5)
    assert not key_found(PROJECT, service_account, key_id)
