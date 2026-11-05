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

from .. import create_instance_private_vpc

PROJECT_ID = "test-project"
LOCATION_ID = "us-west1-b"
INSTANCE_ID = "example-private-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"


@mock.patch.object(notebooks_v2, "NotebookServiceClient", autospec=True)
def test_create_instance_private_vpc_success(
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
            machine_type="e2-standard-4",
            disable_public_ip=True,
        ),
    )
    mock_client.create_instance.return_value = operation

    create_instance_private_vpc.create_instance_private_vpc(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    request = mock_client.create_instance.call_args.kwargs["request"]
    assert request.parent == f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
    assert request.instance_id == INSTANCE_ID
    gce_setup = request.instance.gce_setup
    region_id = "-".join(LOCATION_ID.split("-")[:-1])
    network_interface = gce_setup.network_interfaces[0]
    assert gce_setup.disable_public_ip
    assert network_interface.network == (
        f"projects/{PROJECT_ID}/global/networks/example-network"
    )
    assert network_interface.subnet == (
        f"projects/{PROJECT_ID}/regions/{region_id}/subnetworks/example-subnet"
    )

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Disable Public IP: True" in captured.out
    assert "State: ACTIVE" in captured.out
    assert captured.err == ""


@mock.patch.object(notebooks_v2, "NotebookServiceClient", autospec=True)
def test_create_instance_private_vpc_already_exists(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.create_instance.side_effect = exceptions.AlreadyExists(
        "Instance already exists"
    )

    create_instance_private_vpc.create_instance_private_vpc(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err
