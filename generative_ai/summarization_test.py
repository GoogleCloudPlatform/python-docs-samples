# Copyright 2023 Google LLC
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

import backoff
from google.api_core.exceptions import ResourceExhausted

import summarization


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
_LOCATION = "us-central1"


expected_response = """The efficient-market hypothesis (EMH) states that asset prices reflect all available information.
A direct implication is that it is impossible to "beat the market" consistently on a risk-adjusted basis."""


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_text_summarization() -> None:
    content = summarization.text_summarization(
        temperature=0, project_id=_PROJECT_ID, location=_LOCATION
    )
    assert content == expected_response
