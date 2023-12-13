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

import function_calling


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
_LOCATION = "us-central1"


function_expected_responses = [
    "candidates",
    "content"
    "function_call",
    "get_current_weather",
    "args",
    "fields",
    "location",
    "Boston",
]


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_interview() -> None:
    content = function_calling.generate_function_call(
        prompt="What is the weather like in Boston?"
    )
    assert all(x in content for x in function_expected_responses)
