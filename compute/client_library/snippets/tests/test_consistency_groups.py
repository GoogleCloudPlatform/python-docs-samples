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

from .test_disks import autodelete_regional_blank_disk  # noqa: F401
from ..disks.consistency_groups.add_disk_consistency_group import (
    add_disk_consistency_group,
)
from ..disks.consistency_groups.create_consistency_group import create_consistency_group
from ..disks.consistency_groups.delete_consistency_group import delete_consistency_group
from ..disks.consistency_groups.list_disks_consistency_group import (
    list_disks_consistency_group,
)
from ..disks.consistency_groups.remove_disk_consistency_group import (
    remove_disk_consistency_group,
)


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "europe-west2"
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


def test_add_remove_and_list_disks_consistency_group(
    autodelete_consistency_group, autodelete_regional_blank_disk  # noqa: F811
):
    # Add disk to consistency group
    add_disk_consistency_group(
        project_id=PROJECT_ID,
        disk_name=autodelete_regional_blank_disk.name,
        disk_location=REGION,
        consistency_group_name=autodelete_consistency_group.name,
        consistency_group_region=REGION,
    )
    disks = list_disks_consistency_group(
        project_id=PROJECT_ID,
        disk_location=REGION,
        consistency_group_name=autodelete_consistency_group.name,
        consistency_group_region=REGION,
    )
    assert any(disk.name == autodelete_regional_blank_disk.name for disk in disks)
    # Remove disk from consistency group
    remove_disk_consistency_group(
        project_id=PROJECT_ID,
        disk_name=autodelete_regional_blank_disk.name,
        disk_location=REGION,
        consistency_group_name=autodelete_consistency_group.name,
        consistency_group_region=REGION,
    )

    # Checking that disk was removed - the list should be empty
    disks = list_disks_consistency_group(
        project_id=PROJECT_ID,
        disk_location=REGION,
        consistency_group_name=autodelete_consistency_group.name,
        consistency_group_region=REGION,
    )
    assert not disks
