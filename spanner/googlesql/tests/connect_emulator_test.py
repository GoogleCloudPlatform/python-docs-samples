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

import os
import runpy
from unittest import mock

from google.api_core import exceptions
import pytest
from spanner_googlesql import connect_emulator

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_connect_with_emulator_creates_missing_resources(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("SPANNER_EMULATOR_HOST", "localhost:9010")
    client = mock_client_class.return_value
    client.project_name = f"projects/{PROJECT_ID}"
    instance = client.instance.return_value
    instance.exists.return_value = False
    database = instance.database.return_value
    database.name = DATABASE_NAME
    database.exists.return_value = False
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1,)]

    connect_emulator.connect_with_emulator(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    instance.create.return_value.result.assert_called_once_with(timeout=60)
    database.create.return_value.result.assert_called_once_with(timeout=60)
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_NAME}" in out
    assert "Emulator Host: localhost:9010" in out
    assert "Query Check: 1" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.AlreadyExists("exists"),
            "error: emulator resource already exists",
        ),
        (
            exceptions.ServiceUnavailable("connection refused"),
            "error: failed to connect to Spanner Emulator",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_connect_with_emulator_errors(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    monkeypatch.setenv("SPANNER_EMULATOR_HOST", "localhost:9010")
    instance = mock_client_class.return_value.instance.return_value
    instance.exists.side_effect = error

    connect_emulator.connect_with_emulator(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)


@mock.patch(SPANNER_CLIENT)
def test_connect_with_emulator_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("SPANNER_EMULATOR_HOST", "localhost:9010")
    instance = mock_client_class.return_value.instance.return_value
    instance.exists.return_value = True
    database = instance.database.return_value
    database.name = DATABASE_NAME
    database.exists.return_value = True
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1,)]
    monkeypatch.setattr(
        "sys.argv",
        [
            "connect_emulator.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_googlesql.connect_emulator", run_name="__main__")

    assert "Query Check: 1" in capsys.readouterr().out


@conftest.live_only
@pytest.mark.skipif(
    not os.environ.get("SPANNER_EMULATOR_HOST"),
    reason="Set SPANNER_EMULATOR_HOST to run live emulator integration test.",
)
def test_connect_with_emulator_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    connect_emulator.connect_with_emulator(
        "emulator-test-project",
        "example-emulator-instance",
        "example-emulator-db",
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Query Check: 1" in out
