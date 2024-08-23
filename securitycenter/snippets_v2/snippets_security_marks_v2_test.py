#!/usr/bin/env python
#
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Demos for working with security marks."""
import os
import random

import pytest

import snippets_security_marks_v2


@pytest.fixture(scope="module")
def organization_id():
    """Gets Organization ID from the environment variable"""
    return os.environ["GCLOUD_ORGANIZATION"]


@pytest.fixture(scope="module")
def asset_name(organization_id):
    """Returns a random asset name from existing assets."""
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()
    # organization_id is the numeric ID of the organization.
    # organization_id=1234567777
    org_name = f"organizations/{organization_id}"
    assets = list(client.list_assets(request={"parent": org_name}))
    # Select a random asset to avoid collision between integration tests.
    asset = (random.sample(assets, 1)[0]).asset.name

    # Set fresh marks.
    update = client.update_security_marks(
        request={
            "security_marks": {
                "name": f"{asset}/securityMarks",
                "marks": {"other": "other_val"},
            }
        }
    )
    assert update.marks == {"other": "other_val"}
    return asset


@pytest.fixture(scope="module")
def source_name(organization_id):
    """Creates a new source in the organization."""
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
    org_name = f"organizations/{organization_id}"
    source = client.create_source(
        request={
            "parent": org_name,
            "source": {
                "display_name": "Security marks Unit test source",
                "description": "A new custom source that does X",
            },
        }
    )
    return source.name


@pytest.fixture(scope="module")
def finding_name(source_name):
    """Creates a new finding and returns it name."""
    from google.cloud import securitycenter_v2
    from google.cloud.securitycenter_v2 import Finding
    from google.protobuf.timestamp_pb2 import Timestamp

    client = securitycenter_v2.SecurityCenterClient()

    now_proto = Timestamp()
    now_proto.GetCurrentTime()

    finding = client.create_finding(
        request={
            "parent": source_name,
            "finding_id": "scfinding",
            "finding": {
                "state": Finding.State.ACTIVE,
                "category": "C1",
                "event_time": now_proto,
                "resource_name": "//cloudresourcemanager.googleapis.com/organizations/1234",
            },
        }
    )
    client.create_finding(
        request={
            "parent": source_name,
            "finding_id": "untouched",
            "finding": {
                "state": Finding.State.ACTIVE,
                "category": "MEDIUM_RISK_ONE",
                "event_time": now_proto,
                "resource_name": "//cloudresourcemanager.googleapis.com/organizations/1234",
            },
        }
    )

    return finding.name


def test_add_to_asset(organization_id, asset_name):
    updated_marks, marks = snippets_security_marks_v2.add_to_asset(organization_id, asset_name.split("/")[-1])
    assert updated_marks.marks.keys() >= marks.keys()


def test_delete_security_marks(organization_id, asset_name):
    updated_marks = snippets_security_marks_v2.delete_security_marks(organization_id, asset_name.split("/")[-1])
    assert "other" in updated_marks.marks
    assert len(updated_marks.marks) == 1


def test_delete_and_update_marks(organization_id, asset_name):
    updated_marks = snippets_security_marks_v2.delete_and_update_marks(organization_id, asset_name.split("/")[-1])
    assert updated_marks.marks == {"key_a": "new_value_for_a", "other": "other_val"}


def test_add_to_finding(organization_id, source_name, finding_name):
    updated_marks, marks = snippets_security_marks_v2.add_to_finding(organization_id, source_name.split("/")[3], "global", finding_name.split("/")[-1])
    assert updated_marks.marks == marks
