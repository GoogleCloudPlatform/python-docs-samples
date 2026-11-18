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
from spanner_instance_admin import delete_instance_config

from . import conftest

PROJECT_ID = "example-project-id"
CUSTOM_ID = "custom-example-nam11"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_delete_instance_config_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    delete_instance_config.delete_instance_config(PROJECT_ID, CUSTOM_ID)

    mock_client_class.return_value.delete_instance_config.assert_called_once()
    out, err = capsys.readouterr()
    assert f"Resource ID: {CUSTOM_ID}" in out
    assert f"Deleted Config: {CUSTOM_ID}" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("missing"),
            "error: custom instance config 'custom-example-nam11'",
        ),
        (
            exceptions.FailedPrecondition("in use"),
            "error: failed to delete custom instance config",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_delete_instance_config_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.delete_instance_config.side_effect = error

    delete_instance_config.delete_instance_config(PROJECT_ID, CUSTOM_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_delete_instance_config_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "delete_instance_config.py",
            "--project-id",
            PROJECT_ID,
            "--custom-config-id",
            CUSTOM_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.delete_instance_config", run_name="__main__"
    )

    assert f"Deleted Config: {CUSTOM_ID}" in capsys.readouterr().out


@conftest.live_only
def test_delete_instance_config_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    cid = f"custom-del-{uuid.uuid4().hex[:6]}"
    cpath = admin.instance_config_path(conftest.LIVE_PROJECT_ID, cid)
    try:
        create_instance_config.create_instance_config(
            conftest.LIVE_PROJECT_ID, cid, "nam11"
        )
        capsys.readouterr()
        delete_instance_config.delete_instance_config(conftest.LIVE_PROJECT_ID, cid)
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Deleted Config: {cid}" in out
    finally:
        try:
            admin.delete_instance_config(name=cpath)
        except exceptions.NotFound:
            pass
