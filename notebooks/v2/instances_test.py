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

from unittest import mock

from google.api_core import exceptions
from google.cloud import notebooks_v2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
import pytest

import check_instance_upgradability
import create_instance
import create_instance_cmek
import create_instance_confidential
import create_instance_custom_container
import create_instance_gpu
import create_instance_hardened
import create_instance_private_vpc
import create_instance_single_user
import delete_instance
import diagnose_instance
import get_instance
import get_instance_iam_policy
import list_instances
import reset_instance
import rollback_instance
import set_instance_iam_policy
import start_instance
import stop_instance
import test_instance_iam_permissions
import update_instance_machine_type
import update_instance_metadata
import update_instance_shielded_config
import upgrade_instance

PROJECT_ID = "example-project"
LOCATION_ID = "us-central1-a"
INSTANCE_ID = "example-instance"
INSTANCE_NAME = (
    f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"
)


def _make_mock_instance(
    name: str = INSTANCE_NAME,
    machine_type: str = "e2-standard-4",
) -> notebooks_v2.Instance:
    return notebooks_v2.Instance(
        name=name,
        id="1234567890",
        creator="example-user@example.com",
        proxy_uri="example-proxy.notebooks.googleusercontent.com",
        state=notebooks_v2.State.ACTIVE,
        health_state=notebooks_v2.HealthState.HEALTHY,
        gce_setup=notebooks_v2.GceSetup(
            machine_type=machine_type,
            disable_public_ip=True,
            metadata={"idle-timeout-seconds": "3600"},
            boot_disk=notebooks_v2.BootDisk(
                disk_size_gb=200,
                disk_encryption=notebooks_v2.DiskEncryption.CMEK,
                kms_key=(
                    f"projects/{PROJECT_ID}/locations/us-central1/"
                    "keyRings/example-key-ring/cryptoKeys/example-key"
                ),
            ),
            container_image=notebooks_v2.ContainerImage(
                repository="gcr.io/deeplearning-platform-release/base-cpu",
                tag="latest",
            ),
            shielded_instance_config=notebooks_v2.ShieldedInstanceConfig(
                enable_secure_boot=True,
                enable_vtpm=True,
                enable_integrity_monitoring=True,
            ),
        ),
    )


def _make_mock_lro(result_obj: object = None) -> mock.MagicMock:
    operation = mock.MagicMock()
    operation.operation.name = (
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/operations/op-123"
    )
    operation.result.return_value = result_obj
    return operation


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_list_instances_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.list_instances.return_value = [_make_mock_instance()]

    list_instances.list_instances(PROJECT_ID, LOCATION_ID)

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "State: ACTIVE" in captured.out
    assert captured.err == ""


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_list_instances_not_found(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.list_instances.side_effect = exceptions.NotFound("Zone not found")

    list_instances.list_instances(PROJECT_ID, LOCATION_ID)

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert LOCATION_ID in captured.err


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_get_instance_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.get_instance.return_value = _make_mock_instance()

    get_instance.get_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Health State: HEALTHY" in captured.out
    assert "State: ACTIVE" in captured.out


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_get_instance_not_found(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.get_instance.side_effect = exceptions.NotFound("Instance missing")

    get_instance.get_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_create_instance_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.create_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )

    create_instance.create_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert "Waiting for operation to complete:" in captured.out
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Machine Type: e2-standard-4" in captured.out


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_create_instance_already_exists(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.create_instance.side_effect = exceptions.AlreadyExists(
        "Duplicate instance"
    )

    create_instance.create_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_stop_start_reset_delete_instance(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.stop_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )
    mock_client.start_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )
    mock_client.reset_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )
    mock_client.delete_instance.return_value = _make_mock_lro(None)

    stop_instance.stop_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)
    start_instance.start_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)
    reset_instance.reset_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)
    delete_instance.delete_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Status: Deleted" in captured.out


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_update_and_maintenance_operations(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.update_instance.return_value = _make_mock_lro(
        _make_mock_instance(machine_type="n1-standard-8")
    )
    mock_client.check_instance_upgradability.return_value = (
        notebooks_v2.CheckInstanceUpgradabilityResponse(
            upgradeable=True,
            upgrade_version="m120",
            upgrade_info="Upgrade available",
            upgrade_image="gcr.io/deeplearning-platform-release/base-cpu:m120",
        )
    )
    mock_client.upgrade_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )
    mock_client.rollback_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )
    mock_client.diagnose_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )

    update_instance_machine_type.update_instance_machine_type(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID, "n1-standard-8"
    )
    update_instance_metadata.update_instance_metadata(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    update_instance_shielded_config.update_instance_shielded_config(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    check_instance_upgradability.check_instance_upgradability(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    upgrade_instance.upgrade_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)
    rollback_instance.rollback_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)
    diagnose_instance.diagnose_instance(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert "Machine Type: n1-standard-8" in captured.out
    assert "Secure Boot Enabled: True" in captured.out
    assert "Upgradeable: True" in captured.out
    assert "Health State: HEALTHY" in captured.out


@mock.patch("google.cloud.notebooks_v2.NotebookServiceClient")
def test_specialized_create_and_iam_operations(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.create_instance.return_value = _make_mock_lro(
        _make_mock_instance()
    )
    mock_policy = policy_pb2.Policy(
        version=1,
        etag=b"etag-1",
        bindings=[
            policy_pb2.Binding(
                role="roles/notebooks.runner",
                members=["user:example-user@example.com"],
            )
        ],
    )
    mock_client.get_iam_policy.return_value = mock_policy
    mock_client.set_iam_policy.return_value = mock_policy
    mock_client.test_iam_permissions.return_value = (
        iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["notebooks.instances.get"]
        )
    )

    create_instance_gpu.create_instance_gpu(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    create_instance_custom_container.create_instance_custom_container(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    create_instance_cmek.create_instance_cmek(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    create_instance_confidential.create_instance_confidential(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    create_instance_private_vpc.create_instance_private_vpc(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    create_instance_single_user.create_instance_single_user(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    create_instance_hardened.create_instance_hardened(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    get_instance_iam_policy.get_instance_iam_policy(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    set_instance_iam_policy.set_instance_iam_policy(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )
    test_instance_iam_permissions.test_instance_iam_permissions(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    captured = capsys.readouterr()
    assert (
        "Container Repository: gcr.io/deeplearning-platform-release/base-cpu"
        in captured.out
    )
    assert "Boot Disk Encryption: CMEK" in captured.out
    assert "Disable Public IP: True" in captured.out
    assert "Creator: example-user@example.com" in captured.out
    assert "Secure Boot Enabled: True" in captured.out
    assert "Role: roles/notebooks.runner" in captured.out
    assert "Allowed Permissions: ['notebooks.instances.get']" in captured.out
