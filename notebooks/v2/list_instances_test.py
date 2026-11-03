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
from google.cloud import notebooks_v2
import pytest

import list_instances

PROJECT_ID = "example-project"
LOCATION_ID = "us-central1-a"
INSTANCE_ID = "example-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_list_instances_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.list_instances.return_value = [
        notebooks_v2.Instance(
            name=INSTANCE_NAME,
            id="1234567890",
            creator="example-user@example.com",
            proxy_uri="example-proxy.notebooks.googleusercontent.com",
            state=notebooks_v2.State.ACTIVE,
        )
    ]

    list_instances.list_instances(PROJECT_ID, LOCATION_ID)

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "State: ACTIVE" in captured.out
    assert captured.err == ""


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_list_instances_not_found(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.list_instances.side_effect = exceptions.NotFound("Zone not found")

    list_instances.list_instances(PROJECT_ID, LOCATION_ID)

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert LOCATION_ID in captured.err
