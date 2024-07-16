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
import re
import uuid

from _pytest.capture import CaptureFixture
import backoff
from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable
from google.cloud import securitycenter_v2
from google.cloud.securitycenter_v2.services.security_center.pagers import (
    ListFindingsPager,
)
import pytest

import snippets_mute_config_v2

# TODO(developer): Replace these variables before running the sample.
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


@pytest.fixture
def mute_rule():
    mute_rule_create = f"random-mute-create-{uuid.uuid4()}"
    mute_rule_update = f"random-mute-update-{uuid.uuid4()}"
    resp_create = snippets_mute_config_v2.create_mute_rule(f"projects/{PROJECT_ID}","global",mute_rule_create)
    resp_update = snippets_mute_config_v2.create_mute_rule(f"projects/{PROJECT_ID}","global",mute_rule_update)

    yield {"create": mute_rule_create, "create_resp": resp_create, "update": mute_rule_update, "update_resp": resp_update}

    snippets_mute_config_v2.delete_mute_rule(
        f"projects/{PROJECT_ID}","global",mute_rule_create
    )
    snippets_mute_config_v2.delete_mute_rule(
        f"projects/{PROJECT_ID}","global",mute_rule_update
    )


@pytest.fixture
def finding(capsys: CaptureFixture):
    import snippets_findings_v2
    from snippets_findings_v2 import create_finding

    snippets_findings_v2.create_source(ORGANIZATION_ID)
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


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_mute_rule(mute_rule):
    response = snippets_mute_config_v2.get_mute_rule(
        f"projects/{PROJECT_ID}","global",mute_rule.get('create')
    )
    assert response.name == mute_rule.get('create_resp').name



@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_mute_rules(mute_rule):
    response = snippets_mute_config_v2.list_mute_rules(f"projects/{PROJECT_ID}","global")
    assert len(list(response))>0


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_mute_rule(mute_rule):
    response = snippets_mute_config_v2.update_mute_rule(
        f"projects/{PROJECT_ID}","global",mute_rule.get('update')
    )
    assert response.name == mute_rule.get('update_resp').name



@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_set_mute_finding(finding):
    finding_path = finding.get("finding1")
    response = snippets_mute_config_v2.set_mute_finding(finding_path)
    assert response.name == finding_path


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_set_unmute_finding(finding):
    finding_path = finding.get("finding1")
    response = snippets_mute_config_v2.set_unmute_finding(finding_path)



@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_bulk_mute_findings(finding):
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