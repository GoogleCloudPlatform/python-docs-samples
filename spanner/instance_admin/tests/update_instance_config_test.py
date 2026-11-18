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
from spanner_instance_admin import update_instance_config

from . import conftest

PROJECT_ID = "example-project-id"
CUSTOM_ID = "custom-example-nam11"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


def _mock_cfg() -> spanner_admin_instance_v1.InstanceConfig:
    return spanner_admin_instance_v1.InstanceConfig(
        name=f"projects/{PROJECT_ID}/instanceConfigs/{CUSTOM_ID}",
        display_name="Old Name",
        labels={"cloud_spanner_samples": "true"},
    )


@mock.patch(ADMIN_CLIENT)
def test_update_instance_config_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.get_instance_config.return_value = _mock_cfg()
    updated = mock.MagicMock(
        display_name="Updated Custom Instance Config",
        labels={"cloud_spanner_samples": "true", "updated": "true"},
    )
    client.update_instance_config.return_value.result.return_value = updated

    update_instance_config.update_instance_config(PROJECT_ID, CUSTOM_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {CUSTOM_ID}" in out
    assert "Display Name: Updated Custom Instance Config" in out
    assert "Label Count: 2" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.NotFound("missing"),
            "error: custom instance config 'custom-example-nam11'",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to update custom instance config",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_update_instance_config_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.get_instance_config.side_effect = error

    update_instance_config.update_instance_config(PROJECT_ID, CUSTOM_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_update_instance_config_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.get_instance_config.return_value = _mock_cfg()
    updated = mock.MagicMock(
        display_name="Updated Custom Instance Config", labels={"updated": "true"}
    )
    client.update_instance_config.return_value.result.return_value = updated
    monkeypatch.setattr(
        "sys.argv",
        [
            "update_instance_config.py",
            "--project-id",
            PROJECT_ID,
            "--custom-config-id",
            CUSTOM_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.update_instance_config", run_name="__main__"
    )

    assert "Display Name: Updated Custom Instance Config" in capsys.readouterr().out


@conftest.live_only
def test_update_instance_config_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    cid = f"custom-upd-{uuid.uuid4().hex[:6]}"
    cpath = admin.instance_config_path(conftest.LIVE_PROJECT_ID, cid)
    try:
        create_instance_config.create_instance_config(
            conftest.LIVE_PROJECT_ID, cid, "nam11"
        )
        capsys.readouterr()
        update_instance_config.update_instance_config(conftest.LIVE_PROJECT_ID, cid)
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Display Name: Updated Custom Instance Config" in out
    finally:
        try:
            admin.delete_instance_config(name=cpath)
        except exceptions.NotFound:
            pass
