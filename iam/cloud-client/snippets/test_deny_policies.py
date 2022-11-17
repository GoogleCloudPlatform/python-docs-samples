# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re

import pytest
from snippets.get_deny_policy import get_deny_policy
from snippets.list_deny_policies import list_deny_policy
from snippets.update_deny_policy import update_deny_policy

PROJECT_ID = os.environ["IAM_PROJECT_ID"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["IAM_CREDENTIALS"]


def test_retrieve_policy(
    capsys: "pytest.CaptureFixture[str]", deny_policy: str
) -> None:
    # Test policy retrieval, given the policy id.
    get_deny_policy(PROJECT_ID, deny_policy)
    out, _ = capsys.readouterr()
    assert re.search(f"Retrieved the deny policy: {deny_policy}", out)


def test_list_policies(capsys: "pytest.CaptureFixture[str]", deny_policy: str) -> None:
    # Check if the created policy is listed.
    list_deny_policy(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert re.search(deny_policy, out)
    assert re.search("Listed all deny policies", out)


def test_update_deny_policy(
    capsys: "pytest.CaptureFixture[str]", deny_policy: str
) -> None:
    # Check if the policy rule is updated.
    policy = get_deny_policy(PROJECT_ID, deny_policy)
    update_deny_policy(PROJECT_ID, deny_policy, policy.etag)
    out, _ = capsys.readouterr()
    assert re.search(f"Updated the deny policy: {deny_policy}", out)
