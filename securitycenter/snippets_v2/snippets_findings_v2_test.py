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
from itertools import chain
import os

import pytest

import snippets_findings_v2


@pytest.fixture(scope="module")
def organization_id():
    """Get Organization ID from the environment variable"""
    return os.environ["GCLOUD_ORGANIZATION"]


@pytest.fixture(scope="module")
def source_name(organization_id):
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
    org_name = f"organizations/{organization_id}"

    source = client.create_source(
        request={
            "parent": org_name,
            "source": {
                "display_name": "Unit test source",
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


def test_list_all_findings(organization_id, finding_name, source_name):
    finding_result_iterator = snippets_findings_v2.list_all_findings(
        organization_id, source_name.split("/")[-1], "global"
    )

    names = []
    for finding_result in finding_result_iterator:
        names.append(finding_result.finding.name)
    assert finding_name in names


def test_list_filtered_findings(organization_id):
    count = snippets_findings_v2.list_filtered_findings(organization_id, "-", "global")
    assert count > 0


def test_group_all_findings(organization_id):
    count = snippets_findings_v2.group_all_findings(organization_id, "-", "global")
    assert count > 0


def test_group_filtered_findings(organization_id):
    count = snippets_findings_v2.group_filtered_findings(organization_id, "-", "global")
    assert count > 0


def test_list_findings_with_security_marks(organization_id):
    count = snippets_findings_v2.list_findings_with_security_marks(
        organization_id, "-", "global"
    )
    assert count > 0


def test_group_findings_by_state(organization_id):
    count = snippets_findings_v2.group_findings_by_state(organization_id, "-", "global")
    assert count > 0


def test_create_finding(organization_id, source_name):
    created_finding = snippets_findings_v2.create_finding(
        organization_id, "global", "samplefindingid", source_name, "MEDIUM_RISK_ONE"
    )
    assert created_finding.name.split("/")[-1] == "samplefindingid"


def test_update_finding(source_name):
    snippets_findings_v2.create_finding(
        organization_id, "global", "samplefindingid2", source_name, "MEDIUM_RISK_ONE"
    )
    updated_finding = snippets_findings_v2.update_finding(source_name, "global")
    source_properties = updated_finding.source_properties
    keys = source_properties.keys()
    assert "s_value" in keys


def test_create_source(organization_id):
    source = snippets_findings_v2.create_source(organization_id)
    assert source.display_name == "Customized Display Name"


def test_get_source(source_name):
    source = snippets_findings_v2.get_source(source_name)
    assert source.name == source_name


def test_list_source(organization_id):
    count = snippets_findings_v2.list_source(organization_id)
    assert count >= 0


def test_update_source(source_name):
    updated = snippets_findings_v2.update_source(source_name)
    assert updated.display_name == "Updated Display Name"


def test_get_iam_policy(organization_id, source_name):
    response = snippets_findings_v2.get_iam_policy(
        organization_id, source_name.split("/")[-1]
    )
    assert response is not None


def test_set_source_iam_policy(organization_id, source_name):
    user_email = "csccclienttest@gmail.com"
    role_id = "roles/securitycenter.findingsEditor"
    updated = snippets_findings_v2.set_source_iam_policy(
        organization_id, source_name.split("/")[-1], user_email, role_id
    )
    assert any(
        member == "user:csccclienttest@gmail.com"
        for member in chain.from_iterable(
            binding.members for binding in updated.bindings
        )
    )


def test_troubleshoot_iam_permissions(organization_id, source_name):
    permissions = ["securitycenter.findings.update"]
    response = snippets_findings_v2.troubleshoot_iam_permissions(
        organization_id, source_name.split("/")[-1], permissions
    )
    assert permissions == response.permissions
