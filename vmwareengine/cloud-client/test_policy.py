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

from google.cloud import vmwareengine_v1

from create_policy import create_network_policy


@mock.patch('google.cloud.vmwareengine_v1.VmwareEngineClient')
def test_create_policy(mock_client_class):
    mock_client = mock_client_class.return_value
    p = create_network_policy("pro", "reg", "1.2.3.4/26")
    mock_client.create_network_policy.assert_called_once()
    assert len(mock_client.create_network_policy.call_args.args) == 1
    request = mock_client.create_network_policy.call_args.args[0]


@mock.patch('google.cloud.vmwareengine_v1.VmwareEngineClient')
def test_delete_policy(mock_client_class):
    mock_client = mock_client_class.return_value


@mock.patch('google.cloud.vmwareengine_v1.VmwareEngineClient')
def test_update_policy(mock_client_class):
    mock_client = mock_client_class.return_value