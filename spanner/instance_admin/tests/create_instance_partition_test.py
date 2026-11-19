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
import uuid

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1
import pytest
from spanner_instance_admin import create_instance_partition

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-ep-instance"
PARTITION_ID = "example-partition"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_instance_partition_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/nam6"
    )
    part = mock.MagicMock(display_name="Example Geo Partition")
    part.state.name = "READY"
    client.create_instance_partition.return_value.result.return_value = part

    create_instance_partition.create_instance_partition(
        PROJECT_ID, INSTANCE_ID, PARTITION_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {PARTITION_ID}" in out
    assert "Partition State: READY" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: instance partition 'example-partition' already exists",
        ),
        (
            exceptions.FailedPrecondition("edition"),
            "error: failed to create instance partition",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_instance_partition_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/nam6"
    )
    client.create_instance_partition.side_effect = error

    create_instance_partition.create_instance_partition(
        PROJECT_ID, INSTANCE_ID, PARTITION_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_instance_partition_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.instance_config_path.return_value = (
        f"projects/{PROJECT_ID}/instanceConfigs/nam6"
    )
    part = mock.MagicMock(display_name="Example Geo Partition")
    part.state.name = "READY"
    client.create_instance_partition.return_value.result.return_value = part
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_instance_partition.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--instance-partition-id",
            PARTITION_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.create_instance_partition", run_name="__main__"
    )

    assert "Partition State: READY" in capsys.readouterr().out


@conftest.live_only
def test_create_instance_partition_live(capsys: pytest.CaptureFixture[str]) -> None:
    required = ("SPANNER_MR_INSTANCE_ID",)
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    ep_inst = os.environ["SPANNER_MR_INSTANCE_ID"]
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    part_id = f"example-prt-{uuid.uuid4().hex[:6]}"
    part_path = (
        f"projects/{conftest.LIVE_PROJECT_ID}/instances/{ep_inst}"
        f"/instancePartitions/{part_id}"
    )
    try:
        create_instance_partition.create_instance_partition(
            conftest.LIVE_PROJECT_ID, ep_inst, part_id
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Partition State: READY" in out
    finally:
        try:
            admin.delete_instance_partition(name=part_path)
        except exceptions.NotFound:
            pass
