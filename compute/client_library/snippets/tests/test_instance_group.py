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

import pytest

from ..instance_templates.create import create_template
from ..instance_templates.delete import delete_instance_template
from ..instances.managed_instance_group.create import create_managed_instance_group
from ..instances.managed_instance_group.delete import delete_managed_instance_group


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "europe-west2"
ZONE = f"{REGION}-a"


@pytest.fixture()
def autodelete_template():
    template_name = "test-template" + uuid.uuid4().hex[:5]
    yield create_template(PROJECT_ID, template_name)
    delete_instance_template(PROJECT_ID, template_name)


def test_create_managed_instance_group(autodelete_template):
    template_name = autodelete_template.self_link
    group_name = "test-group" + uuid.uuid4().hex[:5]
    size = 3
    instance_group = create_managed_instance_group(
        PROJECT_ID, ZONE, group_name, size, template_name
    )

    assert instance_group.name == group_name
    assert instance_group.target_size == size
    assert instance_group.instance_template == template_name

    delete_managed_instance_group(PROJECT_ID, ZONE, group_name)
