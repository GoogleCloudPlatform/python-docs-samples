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
from spanner_googlesql import disable_leader_aware_routing

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_disable_leader_aware_routing_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.route_to_leader_enabled = False
    database = client.instance.return_value.database.return_value
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1,)]

    disable_leader_aware_routing.disable_leader_aware_routing(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    mock_client_class.assert_called_once_with(
        project=PROJECT_ID, route_to_leader_enabled=False
    )
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Check Result: 1" in out
    assert "Leader-Aware Routing Enabled: False" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: query failed with leader-aware routing disabled",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_disable_leader_aware_routing_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.side_effect = error

    disable_leader_aware_routing.disable_leader_aware_routing(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_disable_leader_aware_routing_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.route_to_leader_enabled = False
    database = client.instance.return_value.database.return_value
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1,)]
    monkeypatch.setattr(
        "sys.argv",
        [
            "disable_leader_aware_routing.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_googlesql.disable_leader_aware_routing", run_name="__main__"
    )

    assert "Leader-Aware Routing Enabled: False" in capsys.readouterr().out


@conftest.live_only
def test_disable_leader_aware_routing_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    disable_leader_aware_routing.disable_leader_aware_routing(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Leader-Aware Routing Enabled: False" in out
