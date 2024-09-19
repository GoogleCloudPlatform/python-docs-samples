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
import os

import backoff
from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable

import pytest

import mute_findings_v2

# TODO(developer): Replace these variables before running the sample.
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]


@pytest.fixture
def finding():
    import snippets_findings_v2
    from snippets_findings_v2 import create_finding

    response = snippets_findings_v2.create_source(ORGANIZATION_ID)
    source_name = response.name
    finding1_path = create_finding(
        ORGANIZATION_ID, "global", "1testingscc", source_name, "MEDIUM_RISK_ONE"
    ).name
    finding2_path = create_finding(
        ORGANIZATION_ID, "global", "2testingscc", source_name, "MEDIUM_RISK_ONE"
    ).name

    yield {
        "source": source_name,
        "finding1": finding1_path,
        "finding2": finding2_path,
    }


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_set_mute_finding(finding):
    finding_path = finding.get("finding1")
    response = mute_findings_v2.set_mute_finding(finding_path)
    assert response.name == finding_path
    assert response.mute.name == "MUTED"


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_set_unmute_finding(finding):
    finding_path = finding.get("finding1")
    response = mute_findings_v2.set_unmute_finding(finding_path)
    assert response.mute.name == "UNMUTED"


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_bulk_mute_findings(finding):
    # Mute findings that belong to this project.
    response = mute_findings_v2.bulk_mute_findings(
        f"organizations/{ORGANIZATION_ID}",
        "global",
        f'resource.project_display_name="{ORGANIZATION_ID}"',
    )
    assert response.done
