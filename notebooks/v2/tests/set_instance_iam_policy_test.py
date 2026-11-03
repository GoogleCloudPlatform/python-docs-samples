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
from google.iam.v1 import policy_pb2
import pytest

from .. import set_instance_iam_policy

PROJECT_ID = "test-project"
LOCATION_ID = "us-west1-b"
INSTANCE_ID = "example-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_set_instance_iam_policy_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    existing_binding = policy_pb2.Binding(
        role="roles/notebooks.admin",
        members=["user:existing-admin@example.com"],
    )
    mock_client.get_iam_policy.return_value = policy_pb2.Policy(
        version=1,
        etag=b"etag-1",
        bindings=[existing_binding],
    )
    mock_client.set_iam_policy.side_effect = lambda request: request.policy

    set_instance_iam_policy.set_instance_iam_policy(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    get_request = mock_client.get_iam_policy.call_args.kwargs["request"]
    assert get_request.resource == INSTANCE_NAME
    set_request = mock_client.set_iam_policy.call_args.kwargs["request"]
    assert set_request.resource == INSTANCE_NAME
    # The etag from the read must be sent back so concurrent edits are rejected.
    assert set_request.policy.etag == b"etag-1"
    bindings = {(b.role, tuple(b.members)) for b in set_request.policy.bindings}
    assert bindings == {
        ("roles/notebooks.admin", ("user:existing-admin@example.com",)),
        ("roles/notebooks.runner", ("user:example-user@example.com",)),
    }

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Bindings Count: 2" in captured.out
    assert captured.err == ""


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_set_instance_iam_policy_not_found(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.get_iam_policy.side_effect = exceptions.NotFound("Instance not found")

    set_instance_iam_policy.set_instance_iam_policy(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    mock_client.set_iam_policy.assert_not_called()
    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err
