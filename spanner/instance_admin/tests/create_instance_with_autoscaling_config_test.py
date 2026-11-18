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
from spanner_instance_admin import create_instance_with_autoscaling_config

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-autoscaling-instance"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_instance_with_autoscaling_config_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/regional-us-central1"
    )
    created = mock.MagicMock()
    created.autoscaling_config.autoscaling_limits.min_nodes = 1
    created.autoscaling_config.autoscaling_limits.max_nodes = 2
    client.create_instance.return_value.result.return_value = created

    create_instance_with_autoscaling_config.create_instance_with_autoscaling_config(
        PROJECT_ID, INSTANCE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_ID}" in out
    assert "Max Nodes: 2" in out
    assert "Min Nodes: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: instance 'example-autoscaling-instance' already exists",
        ),
        (
            exceptions.InvalidArgument("bad limits"),
            "error: failed to create autoscaling instance",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_instance_with_autoscaling_config_errors(
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

    create_instance_with_autoscaling_config.create_instance_with_autoscaling_config(
        PROJECT_ID, INSTANCE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_instance_with_autoscaling_config_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/regional-us-central1"
    )
    created = mock.MagicMock()
    created.autoscaling_config.autoscaling_limits.min_nodes = 1
    created.autoscaling_config.autoscaling_limits.max_nodes = 2
    client.create_instance.return_value.result.return_value = created
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_instance_with_autoscaling_config.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.create_instance_with_autoscaling_config",
        run_name="__main__",
    )

    assert "Max Nodes: 2" in capsys.readouterr().out


@conftest.live_only
def test_create_instance_with_autoscaling_config_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    temp_id = f"example-asc-{uuid.uuid4().hex[:6]}"
    inst_path = admin.instance_path(conftest.LIVE_PROJECT_ID, temp_id)
    try:
        create_instance_with_autoscaling_config.create_instance_with_autoscaling_config(
            conftest.LIVE_PROJECT_ID, temp_id
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Max Nodes: 2" in out
        assert "Min Nodes: 1" in out
    finally:
        try:
            admin.delete_instance(name=inst_path)
        except exceptions.NotFound:
            pass
