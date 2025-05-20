# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import thinking_budget_with_txt
import thinking_includethoughts_with_txt
import thinking_with_txt

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"  # "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


def test_thinking_budget_with_txt() -> None:
    assert thinking_budget_with_txt.generate_content()


def test_thinking_includethoughts_with_txt() -> None:
    assert thinking_includethoughts_with_txt.generate_content()


def test_thinking_with_txt() -> None:
    assert thinking_with_txt.generate_content()
