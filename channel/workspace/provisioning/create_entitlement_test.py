# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

import pytest

from create_entitlement import main

ACCOUNT_ID = os.environ['CHANNEL_RESELLER_ACCOUNT_ID']
ADMIN_USER = os.environ['CHANNEL_RESELLER_ADMIN_USER']
PARENT_DOMAIN = os.environ['CHANNEL_CUSTOMER_PARENT_DOMAIN']
KEY_FILE = os.environ['CHANNEL_JSON_KEY_FILE']


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_main(capsys: pytest.CaptureFixture) -> None:
    account_name = "accounts/" + ACCOUNT_ID
    customer_domain = f'goog-test.ci.{uuid.uuid4().hex}.{PARENT_DOMAIN}'
    main(account_name, ADMIN_USER, customer_domain, KEY_FILE)

    out, _ = capsys.readouterr()

    assert "=== Created client" in out
    assert "=== Selected offer" in out
    assert "=== Created customer" in out
    assert "=== Provisioned cloud identity" in out
    assert "=== Created entitlement" in out
    assert "=== Suspended entitlement" in out
    assert "=== Transfered entitlement" in out
    assert "=== Deleted customer" in out
