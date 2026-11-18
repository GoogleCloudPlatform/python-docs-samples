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

from google.api_core import exceptions
import pytest
from spanner_instance_admin import get_instance_config

from . import conftest

PROJECT_ID = "example-project-id"
CONFIG_ID = "nam3"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_get_instance_config_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg = mock.MagicMock(
        display_name="us-east4/us-east1/us-central1",
        leader_options=["us-east4", "us-central1"],
        replicas=[mock.MagicMock(), mock.MagicMock()],
    )
    mock_client_class.return_value.get_instance_config.return_value = cfg

    get_instance_config.get_instance_config(PROJECT_ID, CONFIG_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {CONFIG_ID}" in out
    assert "Leader Options: ['us-east4', 'us-central1']" in out
    assert "Replica Count: 2" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: instance config 'nam3'"),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to get instance config 'nam3'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_get_instance_config_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.get_instance_config.side_effect = error

    get_instance_config.get_instance_config(PROJECT_ID, CONFIG_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_get_instance_config_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = mock.MagicMock(display_name="nam3", leader_options=["us-east4"], replicas=[])
    mock_client_class.return_value.get_instance_config.return_value = cfg
    monkeypatch.setattr(
        "sys.argv",
        [
            "get_instance_config.py",
            "--project-id",
            PROJECT_ID,
            "--instance-config-id",
            CONFIG_ID,
        ],
    )

    runpy.run_module("spanner_instance_admin.get_instance_config", run_name="__main__")

    assert "Resource ID: nam3" in capsys.readouterr().out


@conftest.live_only
def test_get_instance_config_live(capsys: pytest.CaptureFixture[str]) -> None:
    get_instance_config.get_instance_config(conftest.LIVE_PROJECT_ID, "nam3")
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "us-east4" in out
