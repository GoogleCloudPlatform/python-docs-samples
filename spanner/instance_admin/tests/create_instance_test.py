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

import runpy
from unittest import mock
import uuid

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1
import pytest
from spanner_instance_admin import create_instance

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_instance_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/regional-us-central1"
    )
    created = mock.MagicMock(display_name="Example Spanner Instance", node_count=1)
    created.state.name = "READY"
    client.create_instance.return_value.result.return_value = created

    create_instance.create_instance(PROJECT_ID, INSTANCE_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_ID}" in out
    assert "Instance State: READY" in out
    assert "Node Count: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: instance 'example-instance' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to create instance 'example-instance'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_instance_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/regional-us-central1"
    )
    client.create_instance.side_effect = error

    create_instance.create_instance(PROJECT_ID, INSTANCE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_instance_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/regional-us-central1"
    )
    created = mock.MagicMock(display_name="Example Spanner Instance", node_count=1)
    created.state.name = "READY"
    client.create_instance.return_value.result.return_value = created
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_instance.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
        ],
    )

    runpy.run_module("spanner_instance_admin.create_instance", run_name="__main__")

    assert "Instance State: READY" in capsys.readouterr().out


@conftest.live_only
def test_create_instance_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    temp_id = f"example-ins-{uuid.uuid4().hex[:6]}"
    inst_path = admin.instance_path(conftest.LIVE_PROJECT_ID, temp_id)
    try:
        create_instance.create_instance(conftest.LIVE_PROJECT_ID, temp_id)
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Instance State: READY" in out
    finally:
        try:
            admin.delete_instance(name=inst_path)
        except exceptions.NotFound:
            pass
