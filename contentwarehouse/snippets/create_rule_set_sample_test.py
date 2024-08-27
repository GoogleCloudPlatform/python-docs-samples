# # Copyright 2023 Google LLC
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
#

import os

from contentwarehouse.snippets import create_rule_set_sample
from contentwarehouse.snippets import test_utilities
import pytest

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"


@pytest.mark.skip(
    "Document AI Warehouse is deprecated and will no longer be available on Google Cloud after January 16, 2025."
)
def test_create_rule_set(capsys: pytest.CaptureFixture) -> None:
    project_number = test_utilities.get_project_number(project_id)
    create_rule_set_sample.create_rule_set(
        project_number=project_number,
        location=location,
    )
    out, _ = capsys.readouterr()

    assert "Rule Set Created" in out
    assert "Rule Sets" in out
