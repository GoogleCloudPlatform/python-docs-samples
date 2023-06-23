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

from cancel_private_cloud_deletion import cancel_private_cloud_deletion
from cancel_private_cloud_deletion import cancel_private_cloud_deletion_by_full_name


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_cancel(mock_client_class):
    mock_client = mock_client_class.return_value

    cancel_private_cloud_deletion_by_full_name("test_name")
    request = vmwareengine_v1.UndeletePrivateCloudRequest()
    request.name = "test_name"

    mock_client.undelete_private_cloud.assert_called_once_with(request)

    mock_client.undelete_private_cloud.reset_mock()

    cancel_private_cloud_deletion("project_321", "zone-33", "cloud-number-nine")
    request.name = (
        "projects/project_321/locations/zone-33/privateClouds/cloud-number-nine"
    )
    mock_client.undelete_private_cloud.assert_called_once_with(request)
