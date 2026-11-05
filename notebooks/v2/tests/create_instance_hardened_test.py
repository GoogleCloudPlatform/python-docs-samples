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
import pytest

from .. import create_instance_hardened

PROJECT_ID = "test-project"
LOCATION_ID = "us-west1-b"
INSTANCE_ID = "example-hardened-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"


@mock.patch.object(notebooks_v2, "NotebookServiceClient", autospec=True)
def test_create_instance_hardened_success(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    operation = mock.MagicMock()
    operation.operation.name = (
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/operations/op-123"
    )
    operation.result.return_value = notebooks_v2.Instance(
        name=INSTANCE_NAME,
        state=notebooks_v2.State.ACTIVE,
        gce_setup=notebooks_v2.GceSetup(
            disable_public_ip=True,
            boot_disk=notebooks_v2.BootDisk(
                disk_encryption=notebooks_v2.DiskEncryption.CMEK
            ),
            shielded_instance_config=notebooks_v2.ShieldedInstanceConfig(
                enable_secure_boot=True,
                enable_vtpm=True,
                enable_integrity_monitoring=True,
            ),
        ),
    )
    mock_client.create_instance.return_value = operation

    custom_sa_email = "custom-workbench-sa@shared-project.iam.gserviceaccount.com"
    create_instance_hardened.create_instance_hardened(
        PROJECT_ID,
        LOCATION_ID,
        INSTANCE_ID,
        service_account_email=custom_sa_email,
    )

    request = mock_client.create_instance.call_args.kwargs["request"]
    region_id = "-".join(LOCATION_ID.split("-")[:-1])
    expected_kms_key = (
        f"projects/{PROJECT_ID}/locations/{region_id}/"
        "keyRings/example-key-ring/cryptoKeys/example-key"
    )
    actual_request = notebooks_v2.CreateInstanceRequest.to_dict(
        request,
        always_print_fields_with_no_presence=False,
        use_integers_for_enums=False,
    )
    assert actual_request == {
        "parent": f"projects/{PROJECT_ID}/locations/{LOCATION_ID}",
        "instance_id": INSTANCE_ID,
        "instance": {
            "instance_owners": ["example-user@example.com"],
            "gce_setup": {
                "machine_type": "e2-standard-4",
                "disable_public_ip": True,
                "service_accounts": [{"email": custom_sa_email}],
                "boot_disk": {
                    "disk_size_gb": "150",
                    "disk_type": "PD_SSD",
                    "disk_encryption": "CMEK",
                    "kms_key": expected_kms_key,
                },
                "data_disks": [
                    {
                        "disk_size_gb": "100",
                        "disk_type": "PD_SSD",
                        "disk_encryption": "CMEK",
                        "kms_key": expected_kms_key,
                    }
                ],
                "network_interfaces": [
                    {
                        "network": (
                            f"projects/{PROJECT_ID}/global/networks/example-network"
                        ),
                        "subnet": (
                            f"projects/{PROJECT_ID}/regions/{region_id}/"
                            "subnetworks/example-subnet"
                        ),
                        "nic_type": "GVNIC",
                    }
                ],
                "shielded_instance_config": {
                    "enable_secure_boot": True,
                    "enable_vtpm": True,
                    "enable_integrity_monitoring": True,
                },
                "metadata": {
                    "notebook-disable-root": "true",
                    "notebook-disable-downloads": "true",
                    "notebook-disable-terminal": "true",
                    "serial-port-enable": "false",
                    "block-project-ssh-keys": "true",
                },
            },
        },
    }

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Disable Public IP: True" in captured.out
    assert "Secure Boot Enabled: True" in captured.out
    assert "State: ACTIVE" in captured.out
    assert captured.err == ""


@mock.patch.object(notebooks_v2, "NotebookServiceClient", autospec=True)
def test_create_instance_hardened_already_exists(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.create_instance.side_effect = exceptions.AlreadyExists(
        "Instance already exists"
    )

    create_instance_hardened.create_instance_hardened(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err
