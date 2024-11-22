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

from ..disks.сonsistency_groups.create_consistency_group import create_consistency_group
from ..disks.сonsistency_groups.delete_consistency_group import delete_consistency_group


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"
DESCRIPTION = "Test description"


@pytest.fixture()
def autodelete_consistency_group():
    consistency_group_name = "test-consistency-group" + uuid.uuid4().hex[:5]
    yield create_consistency_group(
        PROJECT_ID, REGION, consistency_group_name, DESCRIPTION
    )
    delete_consistency_group(PROJECT_ID, REGION, consistency_group_name)


def test_create_consistency_group(autodelete_consistency_group) -> None:
    assert autodelete_consistency_group.status == "READY"


def test_delete_consistency_group() -> None:
    group_name = "test-consistency-group-to-delete" + uuid.uuid4().hex[:3]
    group = create_consistency_group(PROJECT_ID, REGION, group_name, DESCRIPTION)
    try:
        assert group.name == group_name
        assert group.status == "READY"
    finally:
        delete_consistency_group(PROJECT_ID, REGION, group_name)
