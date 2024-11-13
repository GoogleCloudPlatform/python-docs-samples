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
import uuid

import backoff
from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable
import pytest

import snippets_mute_config_v2

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


@pytest.fixture
def mute_rule():
    mute_rule_create = f"random-mute-create-{uuid.uuid4()}"
    mute_rule_update = f"random-mute-update-{uuid.uuid4()}"
    resp_create = snippets_mute_config_v2.create_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_create
    )
    resp_update = snippets_mute_config_v2.create_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_update
    )

    yield {
        "create": mute_rule_create,
        "create_resp": resp_create,
        "update": mute_rule_update,
        "update_resp": resp_update,
    }

    snippets_mute_config_v2.delete_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_create
    )
    snippets_mute_config_v2.delete_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_update
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_create_mute_rule():
    mute_rule_create = f"random-mute-create-{uuid.uuid4()}"
    response = snippets_mute_config_v2.create_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_create
    )
    assert mute_rule_create in response.name
    snippets_mute_config_v2.delete_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_create
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_mute_rule(mute_rule):
    response = snippets_mute_config_v2.get_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule.get("create")
    )
    assert response.name == mute_rule.get("create_resp").name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_mute_rules(mute_rule):
    response = snippets_mute_config_v2.list_mute_rules(
        f"projects/{PROJECT_ID}", "global"
    )
    rule_names = [rule.name for rule in response]
    assert mute_rule.get("create_resp").name in rule_names
    assert mute_rule.get("update_resp").name in rule_names


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_mute_rule(mute_rule):
    response = snippets_mute_config_v2.update_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule.get("update")
    )
    assert response.description == "Updated mute config description"


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_delete_mute_rule():
    mute_rule_create = f"random-mute-create-{uuid.uuid4()}"
    snippets_mute_config_v2.create_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_create
    )
    snippets_mute_config_v2.delete_mute_rule(
        f"projects/{PROJECT_ID}", "global", mute_rule_create
    )
