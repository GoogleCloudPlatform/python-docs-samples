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
import random
import uuid

import google.auth
import pytest

from ..instances.custom_hostname.create import create_instance_custom_hostname
from ..instances.custom_hostname.get import get_hostname
from ..instances.delete import delete_instance

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "europe-west1-c"


@pytest.fixture
def autodelete_instance_name():
    instance_name = "test-host-instance-" + uuid.uuid4().hex[:10]

    yield instance_name

    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


@pytest.fixture
def random_hostname():
    yield "instance.{}.hostname".format(random.randint(0, 2 ** 10))


def test_custom_hostname(autodelete_instance_name, random_hostname):
    instance = create_instance_custom_hostname(
        PROJECT, INSTANCE_ZONE, autodelete_instance_name, random_hostname
    )
    assert instance.name == autodelete_instance_name
    assert instance.hostname == random_hostname
    assert (
        get_hostname(PROJECT, INSTANCE_ZONE, autodelete_instance_name)
        == random_hostname
    )
