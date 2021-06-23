# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time

from google.auth import jwt
import pytest
import requests

import vm_identity

AUDIENCE = 'http://www.testing.com'


def wait_for_token(token):
    """
    This function will wait block the Issued At value of the token is in the past.
    It will not validate the token in any way.
    """
    decoded = jwt.decode(token, verify=False)
    time.sleep(max(0, int(decoded['iat']) - int(time.time())))
    return


def test_vm_identity():
    try:
        # Check if we're running in a GCP VM:
        r = requests.get('http://metadata.google.internal/computeMetadata/v1/project/project-id',
                         headers={'Metadata-Flavor': 'Google'})
        project_id = r.text
    except requests.exceptions.ConnectionError:
        # Guess we're not running in a GCP VM, we need to skip this test
        pytest.skip("Test can only be run inside GCE VM.")
        return

    token = vm_identity.acquire_token(AUDIENCE)
    assert isinstance(token, str) and token

    # Because new GCE instances can have their clocks skewed by a lot, we want
    # to make sure we don't try to verify token too soon.
    # https://github.com/GoogleCloudPlatform/python-docs-samples/issues/6156
    wait_for_token(token)

    # Proceed with verification of the received token.
    verification = vm_identity.verify_token(token, AUDIENCE)
    assert isinstance(verification, dict) and verification
    assert verification['aud'] == AUDIENCE
    assert verification['email_verified']
    assert verification['iss'] == 'https://accounts.google.com'
    assert verification['google']['compute_engine']['project_id'] == project_id
