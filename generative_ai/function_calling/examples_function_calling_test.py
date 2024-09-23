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
# TODO: Rename this file after deleting /generative_ai/function_calling_test.py
import advanced_example

import backoff

import basic_example

from google.api_core.exceptions import ResourceExhausted


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
    response = basic_example.generate_function_call()
    assert all(x in str(response.text) for x in summary_expected)
    assert all(x in str(response) for x in response_expected)


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_advanced_function_selection() -> None:
    response = advanced_example.generate_function_call_advanced()
    assert (
        "Pixel 8 Pro 128GB"
        in response.candidates[0].function_calls[0].args["product_name"]
    )
