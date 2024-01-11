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

import backoff
from google.api_core.exceptions import ResourceExhausted

import code_completion_test_function


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_completion_test_function() -> None:
    content = code_completion_test_function.complete_test_function(temperature=0).text
    # every function def ends with `:`
    assert content.startswith(":")
    # test functions use `assert` for validations
    assert "assert" in content
    # test function should `reverse_string` at-least once
    assert "reverse_string" in content
