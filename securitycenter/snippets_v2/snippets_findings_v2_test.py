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



def test_list_all_findings(organization_id):
    count = snippets_findings_v2.list_all_findings(organization_id, "global")
    assert count > 0


def test_list_filtered_findings(organization_id):
    source_name = f"organizations/{organization_id}/sources/-/locations/global"
    count = snippets_findings_v2.list_filtered_findings(source_name)
    assert count > 0


def test_group_all_findings(organization_id):
    count = snippets_findings_v2.group_all_findings(organization_id, "global")
    assert count > 0


def test_group_filtered_findings(organization_id):
    source_name = f"organizations/{organization_id}/sources/-/locations/global"
    count = snippets_findings_v2.group_filtered_findings(source_name)
    assert count > 0


def test_create_source(organization_id):
    snippets_findings_v2.create_source(organization_id)


def test_get_source(source_name):
    source = snippets_findings_v2.get_source(source_name)
    assert source.name == source_name


def test_list_source(organization_id):
    count = snippets_findings_v2.list_source(organization_id)
    assert count >= 0


def test_update_source(source_name):
    updated = snippets_findings_v2.update_source(source_name)
    assert updated.display_name == "Updated Display Name"