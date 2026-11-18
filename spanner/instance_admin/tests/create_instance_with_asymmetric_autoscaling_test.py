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
from spanner_instance_admin import create_instance_with_asymmetric_autoscaling

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-asym-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_instance_v1.InstanceAdminClient"


def _fake_created_instance() -> spanner_admin_instance_v1.Instance:
    return spanner_admin_instance_v1.Instance(
        name=INSTANCE_NAME,
        display_name="Asymmetric Autoscaling",
        state=spanner_admin_instance_v1.Instance.State.READY,
        autoscaling_config=spanner_admin_instance_v1.AutoscalingConfig(
            asymmetric_autoscaling_options=[
                spanner_admin_instance_v1.AutoscalingConfig.AsymmetricAutoscalingOption(
                    replica_selection=spanner_admin_instance_v1.ReplicaSelection(
                        location="us-west1"
                    )
                )
            ]
        ),
    )


@mock.patch(ADMIN_CLIENT)
def test_create_instance_with_asymmetric_autoscaling_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.create_instance.return_value.result.return_value = _fake_created_instance()

    create_instance_with_asymmetric_autoscaling.create_instance_with_asymmetric_autoscaling(
        PROJECT_ID, INSTANCE_ID
    )

    req = client.create_instance.call_args.kwargs["request"]
    assert req.instance_id == INSTANCE_ID
    opts = req.instance.autoscaling_config.asymmetric_autoscaling_options
    assert len(opts) == 1
    assert opts[0].replica_selection.location == "us-west1"

    out, err = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_ID}" in out
    assert PROJECT_ID not in out
    assert "Asymmetric Overrides: 1" in out
    assert "Instance State: READY" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("exists"),
            "error: Spanner instance 'example-asym-instance' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to create asymmetric-autoscaling instance",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_instance_with_asymmetric_autoscaling_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.create_instance.side_effect = error

    create_instance_with_asymmetric_autoscaling.create_instance_with_asymmetric_autoscaling(
        PROJECT_ID, INSTANCE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_instance_with_asymmetric_autoscaling_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.create_instance.return_value.result.return_value = _fake_created_instance()
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_instance_with_asymmetric_autoscaling.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
        ],
    )

    runpy.run_module(
        "spanner_instance_admin.create_instance_with_asymmetric_autoscaling",
        run_name="__main__",
    )

    assert "Asymmetric Overrides: 1" in capsys.readouterr().out


@conftest.live_only
def test_create_instance_with_asymmetric_autoscaling_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    admin = spanner_admin_instance_v1.InstanceAdminClient()
    temp_instance_id = f"example-asym-{uuid.uuid4().hex[:6]}"
    temp_instance_name = (
        f"projects/{conftest.LIVE_PROJECT_ID}/instances/{temp_instance_id}"
    )

    try:
        create_instance_with_asymmetric_autoscaling.create_instance_with_asymmetric_autoscaling(
            conftest.LIVE_PROJECT_ID,
            temp_instance_id,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Resource ID: {temp_instance_id}" in out
        assert "Asymmetric Overrides: 1" in out
    finally:
        try:
            admin.delete_instance(name=temp_instance_name)
        except exceptions.NotFound:
            pass
