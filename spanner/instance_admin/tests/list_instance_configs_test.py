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
from spanner_instance_admin import list_instance_configs

from . import conftest

PROJECT_ID = "example-project-id"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_list_instance_configs_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg = mock.MagicMock(leader_options=["us-central1"])
    cfg.name = f"projects/{PROJECT_ID}/instanceConfigs/regional-us-central1"
    mock_client_class.return_value.list_instance_configs.return_value = [cfg]

    list_instance_configs.list_instance_configs(PROJECT_ID)

    out, err = capsys.readouterr()
    assert "Resource ID: regional-us-central1" in out
    assert "Total Instance Configs: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.PermissionDenied("denied"),
            "error: permission denied listing Spanner instance configs",
        ),
        (
            exceptions.ServiceUnavailable("down"),
            "error: failed to list Spanner instance configs",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_list_instance_configs_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.list_instance_configs.side_effect = error

    list_instance_configs.list_instance_configs(PROJECT_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_list_instance_configs_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.list_instance_configs.return_value = []
    monkeypatch.setattr(
        "sys.argv",
        ["list_instance_configs.py", "--project-id", PROJECT_ID],
    )

    runpy.run_module(
        "spanner_instance_admin.list_instance_configs", run_name="__main__"
    )

    assert "Total Instance Configs: 0" in capsys.readouterr().out


@conftest.live_only
def test_list_instance_configs_live(capsys: pytest.CaptureFixture[str]) -> None:
    list_instance_configs.list_instance_configs(conftest.LIVE_PROJECT_ID)
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Total Instance Configs:" in out
