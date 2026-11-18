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
from spanner_transactions import set_request_tag

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_set_request_tag_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.return_value = [(1, 1, "Total Junk")]

    set_request_tag.set_request_tag(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    req_opts = snapshot.execute_sql.call_args.kwargs["request_options"]
    assert req_opts.request_tag == "app=concert,env=dev,action=select"
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Row Count: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: database 'example-db'"),
        (exceptions.PermissionDenied("denied"), "error: tagged query failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_set_request_tag_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.side_effect = error

    set_request_tag.set_request_tag(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_set_request_tag_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.return_value = [(1, 1, "Total Junk")]
    monkeypatch.setattr(
        "sys.argv",
        [
            "set_request_tag.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_transactions.set_request_tag", run_name="__main__")

    assert "Row Count: 1" in capsys.readouterr().out


@conftest.live_only
def test_set_request_tag_live(capsys: pytest.CaptureFixture[str]) -> None:
    set_request_tag.set_request_tag(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Total Junk" in out
