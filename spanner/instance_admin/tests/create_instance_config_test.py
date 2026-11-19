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
from spanner_instance_admin import create_instance_config

from . import conftest

PROJECT_ID = "example-project-id"
CUSTOM_ID = "custom-example-nam11"
BASE_ID = "nam11"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


def _mock_base_config() -> spanner_admin_instance_v1.InstanceConfig:
    r1 = spanner_admin_instance_v1.ReplicaInfo(location="us-central1")
    opt = spanner_admin_instance_v1.ReplicaInfo(location="us-east1")
    return spanner_admin_instance_v1.InstanceConfig(
        name=f"projects/{PROJECT_ID}/instanceConfigs/{BASE_ID}",
        replicas=[r1],
        optional_replicas=[opt],
    )


@mock.patch(ADMIN_CLIENT)
def test_create_instance_config_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.side_effect = (
        lambda p, c: f"projects/{p}/instanceConfigs/{c}"
    )
    client.get_instance_config.return_value = _mock_base_config()
    created = mock.MagicMock(
        display_name="Custom Python Sample Config", replicas=[1, 2]
    )
    client.create_instance_config.return_value.result.return_value = created

    create_instance_config.create_instance_config(PROJECT_ID, CUSTOM_ID, BASE_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {CUSTOM_ID}" in out
    assert "Replica Count: 2" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: custom instance config 'custom-example-nam11' already exists",
        ),
        (
            exceptions.InvalidArgument("bad name"),
            "error: failed to create custom instance config",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_instance_config_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.side_effect = (
        lambda p, c: f"projects/{p}/instanceConfigs/{c}"
    )
    client.get_instance_config.return_value = _mock_base_config()
    client.create_instance_config.side_effect = error

    create_instance_config.create_instance_config(PROJECT_ID, CUSTOM_ID, BASE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_instance_config_without_optional_replicas(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.side_effect = (
        lambda p, c: f"projects/{p}/instanceConfigs/{c}"
    )
    base_config = _mock_base_config()
    del base_config.optional_replicas[:]
    client.get_instance_config.return_value = base_config

    create_instance_config.create_instance_config(PROJECT_ID, CUSTOM_ID, BASE_ID)

    client.create_instance_config.assert_not_called()
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(
        "error: cannot create custom instance config from base config"
    )
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_instance_config_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_config_path.side_effect = (
        lambda p, c: f"projects/{p}/instanceConfigs/{c}"
    )
    client.get_instance_config.return_value = _mock_base_config()
    created = mock.MagicMock(
        display_name="Custom Python Sample Config", replicas=[1, 2]
    )
    client.create_instance_config.return_value.result.return_value = created
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_instance_config.py",
            "--project-id",
            PROJECT_ID,
            "--custom-config-id",
            CUSTOM_ID,
            "--base-config-id",
            BASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.create_instance_config", run_name="__main__"
    )

    assert "Replica Count: 2" in capsys.readouterr().out


@conftest.live_only
def test_create_instance_config_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    cid = f"custom-example-{uuid.uuid4().hex[:6]}"
    cpath = admin.instance_config_path(conftest.LIVE_PROJECT_ID, cid)
    try:
        create_instance_config.create_instance_config(
            conftest.LIVE_PROJECT_ID, cid, "nam11"
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Resource ID: {cid}" in out
    finally:
        try:
            admin.delete_instance_config(name=cpath)
        except exceptions.NotFound:
            pass
