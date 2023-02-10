#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import uuid

import google.auth
import pytest

from ..instances.delete import delete_instance
from ..instances.spot.create import create_spot_instance
from ..instances.spot.is_spot_vm import is_spot_vm

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "europe-west2-c"


@pytest.fixture
def autodelete_instance_name():
    instance_name = "i" + uuid.uuid4().hex[:10]

    yield instance_name

    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


def test_preemptible_creation(autodelete_instance_name):
    instance = create_spot_instance(
        PROJECT, INSTANCE_ZONE, autodelete_instance_name
    )

    assert instance.name == autodelete_instance_name
    assert is_spot_vm(PROJECT, INSTANCE_ZONE, instance.name)
