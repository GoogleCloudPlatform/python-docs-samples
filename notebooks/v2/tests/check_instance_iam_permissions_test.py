# Copyright 2026 Google LLC
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

from unittest import mock

from google.api_core import exceptions
from google.iam.v1 import iam_policy_pb2
import pytest

from .. import check_instance_iam_permissions

PROJECT_ID = "test-project"
LOCATION_ID = "us-west1-b"
INSTANCE_ID = "example-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_check_instance_iam_permissions_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.test_iam_permissions.return_value = (
        iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["notebooks.instances.get"]
        )
    )

    check_instance_iam_permissions.check_instance_iam_permissions(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    request = mock_client.test_iam_permissions.call_args.kwargs["request"]
    assert request.resource == INSTANCE_NAME
    assert list(request.permissions) == ["notebooks.instances.get"]

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Allowed Permissions: ['notebooks.instances.get']" in captured.out
    assert captured.err == ""


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_check_instance_iam_permissions_not_found(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.test_iam_permissions.side_effect = exceptions.NotFound(
        "Instance not found"
    )

    check_instance_iam_permissions.check_instance_iam_permissions(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err
