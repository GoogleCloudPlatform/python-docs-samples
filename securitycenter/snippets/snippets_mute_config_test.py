#!/usr/bin/env python
#
# Copyright 2022 Google LLC
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
import re
import uuid

from _pytest.capture import CaptureFixture
from google.cloud import securitycenter
from google.cloud.securitycenter_v1.services.security_center.pagers import (
    ListFindingsPager,
)
import pytest

import snippets_mute_config

# TODO(developer): Replace these variables before running the sample.
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


@pytest.fixture
def mute_rule():
    mute_rule_create = f"random-mute-create-{uuid.uuid4()}"
    mute_rule_update = f"random-mute-update-{uuid.uuid4()}"
    snippets_mute_config.create_mute_rule(f"projects/{PROJECT_ID}", mute_rule_create)
    snippets_mute_config.create_mute_rule(f"projects/{PROJECT_ID}", mute_rule_update)

    yield {"create": mute_rule_create, "update": mute_rule_update}

    snippets_mute_config.delete_mute_rule(
        f"projects/{PROJECT_ID}/muteConfigs/{mute_rule_create}"
    )
    snippets_mute_config.delete_mute_rule(
        f"projects/{PROJECT_ID}/muteConfigs/{mute_rule_update}"
    )


@pytest.fixture
def finding(capsys: CaptureFixture):
    import snippets_findings
    from snippets_findings import create_finding

    snippets_findings.create_source(ORGANIZATION_ID)
    out, _ = capsys.readouterr()
    # source_path is of the format: organizations/{ORGANIZATION_ID}/sources/{source_name}
    source_path = out.split(":")[1].strip()
    source_name = source_path.split("/")[3]
    finding1_path = create_finding(source_path, "1testingscc").name
    finding2_path = create_finding(source_path, "2testingscc").name

    yield {
        "source": source_name,
        "finding1": finding1_path,
        "finding2": finding2_path,
    }


def list_all_findings(source_name) -> ListFindingsPager:
    client = securitycenter.SecurityCenterClient()
    return client.list_findings(request={"parent": source_name})


def test_get_mute_rule(capsys: CaptureFixture, mute_rule):
    snippets_mute_config.get_mute_rule(
        f"projects/{PROJECT_ID}/muteConfigs/{mute_rule.get('create')}"
    )
    out, _ = capsys.readouterr()
    assert re.search("Retrieved the mute rule: ", out)
    assert re.search(mute_rule.get("create"), out)


def test_list_mute_rules(capsys: CaptureFixture, mute_rule):
    snippets_mute_config.list_mute_rules(f"projects/{PROJECT_ID}")
    out, _ = capsys.readouterr()
    assert re.search(mute_rule.get("create"), out)
    assert re.search(mute_rule.get("update"), out)


def test_update_mute_rule(capsys: CaptureFixture, mute_rule):
    snippets_mute_config.update_mute_rule(
        f"projects/{PROJECT_ID}/muteConfigs/{mute_rule.get('update')}"
    )
    snippets_mute_config.get_mute_rule(
        f"projects/{PROJECT_ID}/muteConfigs/{mute_rule.get('update')}"
    )
    out, _ = capsys.readouterr()
    assert re.search("Updated mute config description", out)


def test_set_mute_finding(capsys: CaptureFixture, finding):
    finding_path = finding.get("finding1")
    snippets_mute_config.set_mute_finding(finding_path)
    out, _ = capsys.readouterr()
    assert re.search("Mute value for the finding: MUTED", out)


def test_set_unmute_finding(capsys: CaptureFixture, finding):
    finding_path = finding.get("finding1")
    snippets_mute_config.set_unmute_finding(finding_path)
    out, _ = capsys.readouterr()
    assert re.search("Mute value for the finding: UNMUTED", out)


def test_bulk_mute_findings(capsys: CaptureFixture, finding):
    # Mute findings that belong to this project.
    snippets_mute_config.bulk_mute_findings(
        f"projects/{PROJECT_ID}", f'resource.project_display_name="{PROJECT_ID}"'
    )

    # Get all findings in the source to check if they are muted.
    response = list_all_findings(
        f"projects/{PROJECT_ID}/sources/{finding.get('source')}"
    )
    for i, finding in enumerate(response):
        assert finding.finding.mute == securitycenter.Finding.Mute.MUTED
