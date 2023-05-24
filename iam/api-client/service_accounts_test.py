# Copyright 2016 Google Inc. All Rights Reserved.
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
import uuid

from googleapiclient.errors import HttpError
import pytest

import service_accounts


def test_service_accounts(capsys: pytest.CaptureFixture) -> None:
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    name = f'test-{uuid.uuid4().hex[:25]}'

    try:
        acct = service_accounts.create_service_account(
            project_id, name, 'Py Test Account')
        assert 'uniqueId' in acct

        unique_id = acct['uniqueId']
        service_accounts.list_service_accounts(project_id)
        service_accounts.rename_service_account(
            unique_id, 'Updated Py Test Account')
        service_accounts.disable_service_account(unique_id)
        service_accounts.enable_service_account(unique_id)
        service_accounts.delete_service_account(unique_id)
    finally:
        try:
            service_accounts.delete_service_account(unique_id)
        except HttpError as e:
            # We've recently seen 404 error too.
            # It used to return 403, so we keep it too.
            if '403' in str(e) or '404' in str(e):
                print("Ignoring 404/403 error upon cleanup.")
            else:
                raise
