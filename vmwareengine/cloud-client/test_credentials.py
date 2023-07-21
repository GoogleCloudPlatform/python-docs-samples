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

from unittest import mock

from nsx_credentials import get_nsx_credentials
from vcenter_credentials import get_vcenter_credentials


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_vcredentials(mock_client_class):
    mock_client = mock_client_class.return_value
    get_vcenter_credentials("p2", "rrr", "cname")

    mock_client.show_vcenter_credentials.assert_called_once()
    assert len(mock_client.show_vcenter_credentials.call_args[1]) == 1
    name = mock_client.show_vcenter_credentials.call_args[1]["private_cloud"]
    assert name == "projects/p2/locations/rrr/privateClouds/cname"


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_nsx_credentials(mock_client_class):
    mock_client = mock_client_class.return_value
    get_nsx_credentials("p3", "rrrr", "cname")

    mock_client.show_nsx_credentials.assert_called_once()
    assert len(mock_client.show_nsx_credentials.call_args[1]) == 1
    name = mock_client.show_nsx_credentials.call_args[1]["private_cloud"]
    assert name == "projects/p3/locations/rrrr/privateClouds/cname"
