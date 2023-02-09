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
"""Tests for snippets."""

import os

import pytest

import snippets_list_assets


@pytest.fixture(scope="module")
def organization_id():
    """Get Organization ID from the environment variable"""
    return os.environ["GCLOUD_ORGANIZATION"]


def test_list_all_assets(organization_id):
    """Demonstrate listing and printing all assets."""
    count = snippets_list_assets.list_all_assets(organization_id)
    assert count > 0


def list_assets_with_filters(organization_id):
    count = snippets_list_assets.list_all_assets(organization_id)
    assert count > 0


def test_list_assets_with_filters_and_read_time(organization_id):
    count = snippets_list_assets.list_assets_with_filters_and_read_time(organization_id)
    assert count > 0


def test_list_point_in_time_changes(organization_id):
    count = snippets_list_assets.list_point_in_time_changes(organization_id)
    assert count > 0


def test_group_assets(organization_id):
    count = snippets_list_assets.group_assets(organization_id)
    assert count >= 8  # 8 different asset types.


def test_group_filtered_assets(organization_id):
    count = snippets_list_assets.group_filtered_assets(organization_id)
    assert count == 0


def test_group_assets_by_changes(organization_id):
    count = snippets_list_assets.group_assets_by_changes(organization_id)
    assert count >= 0  # only one asset type is a project
