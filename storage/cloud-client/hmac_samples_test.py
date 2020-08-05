# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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
"""
Tests for hmac.py. Requires GOOGLE_CLOUD_PROJECT (valid project) and
HMAC_KEY_TEST_SERVICE_ACCOUNT (valid service account email) env variables to be
set in order to run.
"""


import os

import google.api_core.exceptions
from google.cloud import storage
import pytest

import storage_activate_hmac_key
import storage_create_hmac_key
import storage_deactivate_hmac_key
import storage_delete_hmac_key
import storage_get_hmac_key
import storage_list_hmac_keys

# We are reaching maximum number of HMAC keys on the service account.
# We change the service account based on the value of
# RUN_TESTS_SESSION in noxfile_config.py.
# The reason we can not use multiple project is that our new projects
# are enforced to have
# 'constraints/iam.disableServiceAccountKeyCreation' policy.

PROJECT_ID = os.environ["MAIN_GOOGLE_CLOUD_PROJECT"]
SERVICE_ACCOUNT_EMAIL = os.environ["HMAC_KEY_TEST_SERVICE_ACCOUNT"]
STORAGE_CLIENT = storage.Client(project=PROJECT_ID)


@pytest.fixture(scope="module")
def new_hmac_key():
    """
    Fixture to create a new HMAC key, and to guarantee all keys are deleted at
    the end of the module.

    NOTE: Due to the module scope, test order in this file is significant
    """
    hmac_key, secret = STORAGE_CLIENT.create_hmac_key(
        service_account_email=SERVICE_ACCOUNT_EMAIL, project_id=PROJECT_ID
    )
    yield hmac_key
    # Re-fetch the key metadata in case state has changed during the test.
    hmac_key = STORAGE_CLIENT.get_hmac_key_metadata(
        hmac_key.access_id, project_id=PROJECT_ID
    )
    if hmac_key.state == "DELETED":
        return
    if not hmac_key.state == "INACTIVE":
        hmac_key.state = "INACTIVE"
        hmac_key.update()
    hmac_key.delete()


def test_list_keys(capsys, new_hmac_key):
    hmac_keys = storage_list_hmac_keys.list_keys(PROJECT_ID)
    assert "HMAC Keys:" in capsys.readouterr().out
    assert hmac_keys.num_results >= 1


def test_create_key(capsys):
    hmac_key = storage_create_hmac_key.create_key(
        PROJECT_ID, SERVICE_ACCOUNT_EMAIL
    )
    hmac_key.state = "INACTIVE"
    hmac_key.update()
    hmac_key.delete()
    assert "Key ID:" in capsys.readouterr().out
    assert hmac_key.access_id


def test_get_key(capsys, new_hmac_key):
    hmac_key = storage_get_hmac_key.get_key(new_hmac_key.access_id, PROJECT_ID)
    assert "HMAC key metadata" in capsys.readouterr().out
    assert hmac_key.access_id == new_hmac_key.access_id


def test_activate_key(capsys, new_hmac_key):
    new_hmac_key.state = "INACTIVE"
    new_hmac_key.update()
    hmac_key = storage_activate_hmac_key.activate_key(
        new_hmac_key.access_id, PROJECT_ID
    )
    assert "State: ACTIVE" in capsys.readouterr().out
    assert hmac_key.state == "ACTIVE"


def test_deactivate_key(capsys, new_hmac_key):
    hmac_key = storage_deactivate_hmac_key.deactivate_key(
        new_hmac_key.access_id, PROJECT_ID
    )
    assert "State: INACTIVE" in capsys.readouterr().out
    assert hmac_key.state == "INACTIVE"


def test_delete_key(capsys, new_hmac_key):
    # Due to reuse of the HMAC key for each test function, the previous
    # test has deactivated the key already.
    try:
        new_hmac_key.state = "INACTIVE"
        new_hmac_key.update()
    except google.api_core.exceptions.BadRequest:
        pass

    storage_delete_hmac_key.delete_key(new_hmac_key.access_id, PROJECT_ID)
    assert "The key is deleted" in capsys.readouterr().out
