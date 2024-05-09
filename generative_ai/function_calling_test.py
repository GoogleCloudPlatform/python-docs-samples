# Copyright 2024 Google LLC
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

import pytest

import function_calling


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


summary_expected = [
    "Boston",
]

response_expected = [
    "candidates",
    "content",
    "role",
    "model",
    "parts",
    "Boston",
]


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling() -> None:
    response = function_calling.generate_function_call(project_id=_PROJECT_ID)
    assert all(x in str(response.text) for x in summary_expected)
    assert all(x in str(response) for x in response_expected)


# TODO: Remove skip once b/336973838 is resolved.
@pytest.mark.skip("Service currently returning INVALID_ARGUMENT")
@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_advanced() -> None:
    response = function_calling.generate_function_call_advanced(project_id=_PROJECT_ID)
    assert all(x in str(response.text) for x in summary_expected)
    assert all(x in str(response) for x in response_expected)
