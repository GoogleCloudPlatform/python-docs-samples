# Copyright 2023 Google LLC
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

import google.auth

from nsx_credentials import get_nsx_credentials
from vcenter_credentials import get_vcenter_credentials


PROJECT = google.auth.default()[1]
REGION = os.getenv('VMWARE_REGION', 'asia-northeast1')
CLOUD_NAME = os.getenv('VMWARE_PRIVATE_CLOUD', 'test-cloud-469e53')


def test_vcredentials():
    credentials = get_vcenter_credentials(PROJECT, f"{REGION}-a", CLOUD_NAME)
    assert credentials.username
    assert credentials.password


def test_nsx_credentials():
    credentials = get_nsx_credentials(PROJECT, f"{REGION}-a", CLOUD_NAME)
    assert credentials.username
    assert credentials.password