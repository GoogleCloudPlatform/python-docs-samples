#!/usr/bin/env python
#
# Copyright 2020 Google LLC
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

import snippets_findings


@pytest.fixture(scope="module")
def organization_id():
    """Get Organization ID from the environment variable"""
    return os.environ["GCLOUD_ORGANIZATION"]


@pytest.fixture(scope="module")
def source_name(organization_id):
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()
    org_name = "organizations/{org_id}".format(org_id=organization_id)

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


def test_create_source(organization_id):
    snippets_findings.create_source(organization_id)


def test_get_source(source_name):
    source = snippets_findings.get_source(source_name)
    assert source.name == source_name


def test_update_source(source_name):
    updated = snippets_findings.update_source(source_name)
    assert updated.display_name == "Updated Display Name"


def test_add_user_to_source(source_name):
    binding, updated = snippets_findings.add_user_to_source(source_name)
    assert any(
        member == "user:csccclienttest@gmail.com"
        for member in chain.from_iterable(
            binding.members for binding in updated.bindings
        )
    )


def test_list_source(organization_id):
    count = snippets_findings.list_source(organization_id)
    assert count >= 0


def test_create_finding(source_name):
    created_finding = snippets_findings.create_finding(source_name, "samplefindingid")
    assert len(created_finding.name) > 0


def test_create_finding_with_source_properties(source_name):
    snippets_findings.create_finding_with_source_properties(source_name)


def test_update_finding(source_name):
    snippets_findings.update_finding(source_name)


def test_update_finding_state(source_name):
    snippets_findings.update_finding_state(source_name)


def test_trouble_shoot(source_name):
    snippets_findings.trouble_shoot(source_name)


def test_list_all_findings(organization_id):
    count = snippets_findings.list_all_findings(organization_id)
    assert count > 0


def test_list_filtered_findings(source_name):
    count = snippets_findings.list_filtered_findings(source_name)
    assert count > 0


def list_findings_at_time(source_name):
    count = snippets_findings.list_findings_at_time(source_name)
    assert count == -1


def test_get_iam_policy(source_name):
    snippets_findings.get_iam_policy(source_name)


def test_group_all_findings(organization_id):
    count = snippets_findings.group_all_findings(organization_id)
    assert count > 0


def test_group_filtered_findings(source_name):
    count = snippets_findings.group_filtered_findings(source_name)
    assert count == 0


def test_group_findings_at_time(source_name):
    count = snippets_findings.group_findings_at_time(source_name)
    assert count == -1


def test_group_findings_and_changes(source_name):
    count = snippets_findings.group_findings_and_changes(source_name)
    assert count == 0
