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

import code_generation_function


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_generation_function() -> None:
    content = code_generation_function.generate_a_function(temperature=0).text
    assert "leap year" in content
