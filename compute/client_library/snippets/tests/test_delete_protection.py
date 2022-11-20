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
from ..instances.delete_protection.create import create_protected_instance
from ..instances.delete_protection.get import get_delete_protection
from ..instances.delete_protection.set import set_delete_protection

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "europe-central2-a"


@pytest.fixture
def autodelete_instance_name():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]

    yield instance_name

    if get_delete_protection(PROJECT, INSTANCE_ZONE, instance_name):
        set_delete_protection(PROJECT, INSTANCE_ZONE, instance_name, False)

    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


def test_delete_protection(autodelete_instance_name):
    instance = create_protected_instance(
        PROJECT, INSTANCE_ZONE, autodelete_instance_name
    )
    assert instance.name == autodelete_instance_name

    assert (
        get_delete_protection(PROJECT, INSTANCE_ZONE, autodelete_instance_name) is True
    )

    set_delete_protection(PROJECT, INSTANCE_ZONE, autodelete_instance_name, False)

    assert (
        get_delete_protection(PROJECT, INSTANCE_ZONE, autodelete_instance_name) is False
    )
