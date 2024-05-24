# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict
import uuid

import google.auth
import pytest

import quickstart

PROJECT = google.auth.default()[1]


@pytest.fixture
def config() -> Dict[str, str]:
    config = {
        "instance_id": f"memcache-{uuid.uuid4().hex[:10]}",
        "location_id": "us-central1",
    }
    try:
        yield config
    finally:
        quickstart.delete_instance(PROJECT, **config)


def test_quickstart(capsys: pytest.CaptureFixture, config: Dict[str, str]) -> None:
    quickstart.quickstart(PROJECT, **config)

    out, _ = capsys.readouterr()
    assert f"Instance {config['instance_id']} was created" in out
    assert "New name is: new_name" in out
    assert f"Instance {config['instance_id']} was deleted" in out
