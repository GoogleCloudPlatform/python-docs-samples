# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import uuid

from google.cloud.tpu_v2.types import Node

import pytest

import create_tpu
import create_tpu_with_script
import delete_tpu
import get_tpu

TPU_NAME = "test-tpu-" + uuid.uuid4().hex[:10]
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
ZONE = "us-south1-a"
TPU_TYPE = "v5litepod-1"
TPU_VERSION = "tpu-vm-tf-2.17.0-pjrt"


# Instance of TPU
@pytest.fixture(scope="session")
def tpu_instance() -> Node:
    yield create_tpu.create_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME, TPU_TYPE, TPU_VERSION)
    try:
        delete_tpu.delete_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    except Exception as e:
        print(f"Error during cleanup: {e}")


def test_creating_tpu(tpu_instance: Node) -> None:
    assert tpu_instance.state == Node.State.READY


def test_creating_with_startup_script() -> None:
    tpu_name_with_script = "script-tpu-" + uuid.uuid4().hex[:5]
    try:
        tpu_with_script = create_tpu_with_script.create_cloud_tpu_with_script(
            PROJECT_ID, ZONE, tpu_name_with_script, TPU_TYPE, TPU_VERSION
        )
        assert "--upgrade numpy" in tpu_with_script.metadata["startup-script"]
    finally:
        delete_tpu.delete_cloud_tpu(PROJECT_ID, ZONE, tpu_name_with_script)


def test_get_tpu() -> None:
    tpu = get_tpu.get_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    assert tpu.state == Node.State.READY
    assert tpu.name == f"projects/{PROJECT_ID}/locations/{ZONE}/nodes/{TPU_NAME}"
