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
import uuid

from _pytest.capture import CaptureFixture
import pytest

from create_deny_policy import create_deny_policy
from delete_deny_policy import delete_deny_policy

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


@pytest.fixture
def deny_policy(capsys: CaptureFixture) -> None:
    policy_id = f"limit-project-deletion-{uuid.uuid4()}"

    # Create the Deny policy.
    create_deny_policy(PROJECT_ID, policy_id)

    yield policy_id

    # Delete the Deny policy and assert if deleted.
    delete_deny_policy(PROJECT_ID, policy_id)
    out, _ = capsys.readouterr()
    assert re.search(f"Deleted the deny policy: {policy_id}", out)
