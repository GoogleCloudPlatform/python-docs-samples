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

from .. import create_instance_gpu

PROJECT_ID = "test-project"
LOCATION_ID = "us-west1-b"
INSTANCE_ID = "example-gpu-instance"
INSTANCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/instances/{INSTANCE_ID}"


@mock.patch.object(notebooks_v2, "NotebookServiceClient", autospec=True)
def test_create_instance_gpu_success(
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
        gce_setup=notebooks_v2.GceSetup(machine_type="n1-standard-4"),
    )
    mock_client.create_instance.return_value = operation

    create_instance_gpu.create_instance_gpu(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    request = mock_client.create_instance.call_args.kwargs["request"]
    assert request.parent == f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
    assert request.instance_id == INSTANCE_ID
    gce_setup = request.instance.gce_setup
    accelerator = gce_setup.accelerator_configs[0]
    assert accelerator.type_ == (
        notebooks_v2.AcceleratorConfig.AcceleratorType.NVIDIA_TESLA_T4
    )
    assert accelerator.core_count == 1
    assert gce_setup.gpu_driver_config.enable_gpu_driver

    captured = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_NAME}" in captured.out
    assert "Machine Type: n1-standard-4" in captured.out
    assert "State: ACTIVE" in captured.out
    assert captured.err == ""


@mock.patch.object(notebooks_v2, "NotebookServiceClient", autospec=True)
def test_create_instance_gpu_already_exists(
    mock_client_cls: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.create_instance.side_effect = exceptions.AlreadyExists(
        "Instance already exists"
    )

    create_instance_gpu.create_instance_gpu(PROJECT_ID, LOCATION_ID, INSTANCE_ID)

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert INSTANCE_ID in captured.err
