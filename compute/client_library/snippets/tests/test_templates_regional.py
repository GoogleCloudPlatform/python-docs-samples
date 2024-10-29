# Copyright 2024 Google LLC
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

import os
import uuid

from google.api_core.exceptions import NotFound

import pytest

from ..instance_templates.compute_regional_template import (
    create_compute_regional_template,
    delete_compute_regional_template,
    get_compute_regional_template,
)


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"


@pytest.fixture(scope="function")
def regional_template():
    test_template_name = "test-template-" + uuid.uuid4().hex[:6]
    template = create_compute_regional_template.create_regional_instance_template(
        PROJECT_ID, REGION, test_template_name
    )
    yield template
    delete_compute_regional_template.delete_regional_instance_template(
        PROJECT_ID, REGION, test_template_name
    )


def test_create_regional_template(regional_template):
    assert regional_template.name.startswith("test-template-")


def test_get_regional_template(regional_template):
    template = get_compute_regional_template.get_regional_instance_template(
        PROJECT_ID, REGION, regional_template.name
    )
    assert template.name == regional_template.name


def test_delete_regional_template():
    test_template_name = "test-template-" + uuid.uuid4().hex[:6]
    create_compute_regional_template.create_regional_instance_template(
        PROJECT_ID, REGION, test_template_name
    )
    with pytest.raises(NotFound) as exc_info:
        delete_compute_regional_template.delete_regional_instance_template(
            PROJECT_ID, REGION, test_template_name
        )
        get_compute_regional_template.get_regional_instance_template(
            PROJECT_ID, REGION, test_template_name
        )
    assert "was not found" in str(exc_info.value)
