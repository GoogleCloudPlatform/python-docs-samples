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
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_database_admin import enable_fine_grained_access

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
IAM_MEMBER = "user:alice@example.com"
DB_ROLE = "new_parent"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_enable_fine_grained_access_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    client.set_iam_policy.return_value.version = 3

    enable_fine_grained_access.enable_fine_grained_access(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, IAM_MEMBER, DB_ROLE
    )

    client.set_iam_policy.assert_called_once()
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Database Role: new_parent" in out
    assert "Policy Version: 3" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.InvalidArgument("bad member"),
            "error: invalid IAM principal or conditional binding",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to enable fine-grained access",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_enable_fine_grained_access_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    client.get_iam_policy.side_effect = error

    enable_fine_grained_access.enable_fine_grained_access(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, IAM_MEMBER, DB_ROLE
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_enable_fine_grained_access_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    client.set_iam_policy.return_value.version = 3
    monkeypatch.setattr(
        "sys.argv",
        [
            "enable_fine_grained_access.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--iam-member",
            IAM_MEMBER,
            "--database-role",
            DB_ROLE,
        ],
    )

    runpy.run_module(
        "spanner_database_admin.enable_fine_grained_access", run_name="__main__"
    )

    assert "Policy Version: 3" in capsys.readouterr().out


@conftest.live_only
def test_enable_fine_grained_access_live(capsys: pytest.CaptureFixture[str]) -> None:
    required = ("SPANNER_FGAC_IAM_MEMBER",)
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    iam_member = os.environ["SPANNER_FGAC_IAM_MEMBER"]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    try:
        enable_fine_grained_access.enable_fine_grained_access(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
            iam_member,
            "new_parent",
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Database Role: new_parent" in out
        assert "Policy Version: 3" in out
    finally:
        cur_policy = admin.get_iam_policy(
            request={"resource": db_path, "options": {"requested_policy_version": 3}}
        )
        cur_policy.version = 3
        kept = [
            b for b in cur_policy.bindings if b.condition.title != "fgac_new_parent"
        ]
        del cur_policy.bindings[:]
        cur_policy.bindings.extend(kept)
        admin.set_iam_policy(request={"resource": db_path, "policy": cur_policy})
