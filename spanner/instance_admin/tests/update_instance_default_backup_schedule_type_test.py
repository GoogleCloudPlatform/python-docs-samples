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
from google.cloud import spanner_admin_instance_v1
import pytest
from spanner_instance_admin import update_instance_default_backup_schedule_type

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_update_instance_default_backup_schedule_type_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    updated = mock.MagicMock()
    updated.default_backup_schedule_type.name = "AUTOMATIC"
    client.update_instance.return_value.result.return_value = updated

    update_instance_default_backup_schedule_type.update_instance_default_backup_schedule_type(
        PROJECT_ID, INSTANCE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_ID}" in out
    assert "Default Backup Schedule Type: AUTOMATIC" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (exceptions.NotFound("missing"), "error: instance 'example-instance'"),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to update default_backup_schedule_type",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_update_instance_default_backup_schedule_type_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.update_instance.side_effect = error

    update_instance_default_backup_schedule_type.update_instance_default_backup_schedule_type(
        PROJECT_ID, INSTANCE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_update_instance_default_backup_schedule_type_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    updated = mock.MagicMock()
    updated.default_backup_schedule_type.name = "AUTOMATIC"
    client.update_instance.return_value.result.return_value = updated
    monkeypatch.setattr(
        "sys.argv",
        [
            "update_instance_default_backup_schedule_type.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.update_instance_default_backup_schedule_type",
        run_name="__main__",
    )

    assert "Default Backup Schedule Type: AUTOMATIC" in capsys.readouterr().out


@conftest.live_only
def test_update_instance_default_backup_schedule_type_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    required = ("SPANNER_INSTANCE_ID",)
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    live_inst = os.environ["SPANNER_INSTANCE_ID"]
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    inst_path = admin.instance_path(conftest.LIVE_PROJECT_ID, live_inst)
    orig = admin.get_instance(name=inst_path)
    orig_type = orig.default_backup_schedule_type
    try:
        update_instance_default_backup_schedule_type.update_instance_default_backup_schedule_type(
            conftest.LIVE_PROJECT_ID, live_inst
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Default Backup Schedule Type: AUTOMATIC" in out
    finally:
        schedule_types = spanner_admin_instance_v1.Instance.DefaultBackupScheduleType
        was_unspecified = (
            orig_type == schedule_types.DEFAULT_BACKUP_SCHEDULE_TYPE_UNSPECIFIED
        )
        if orig_type != schedule_types.AUTOMATIC:
            admin.update_instance(
                request=spanner_admin_instance_v1.UpdateInstanceRequest(
                    instance=spanner_admin_instance_v1.Instance(
                        name=inst_path,
                        default_backup_schedule_type=(
                            schedule_types.NONE if was_unspecified else orig_type
                        ),
                    ),
                    field_mask={"paths": ["default_backup_schedule_type"]},
                )
            ).result(timeout=300)
