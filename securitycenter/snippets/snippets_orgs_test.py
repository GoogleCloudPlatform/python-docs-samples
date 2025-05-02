#!/usr/bin/env python
#
# Copyright 2019 Google LLC
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
"""Examples for working with organization settings. """
import os

import backoff
from google.api_core.exceptions import Aborted
import pytest

import snippets_orgs


@pytest.fixture(scope="module")
def organization_id():
    """Get Organization ID from the environment variable"""
    return os.environ["GCLOUD_ORGANIZATION"]


def test_get_settings(organization_id):
    snippets_orgs.get_settings(organization_id)


@backoff.on_exception(backoff.expo, (Aborted,), max_tries=3)
def test_update_asset_discovery_org_settings(organization_id):
    updated = snippets_orgs.update_asset_discovery_org_settings(organization_id)
    assert updated.enable_asset_discovery
