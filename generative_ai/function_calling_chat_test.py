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
# TODO: Delete this file after approving /function_calling/chat_example_test.py

import backoff
from google.api_core.exceptions import ResourceExhausted

import function_calling_chat


summaries_expected = [
    "Pixel 8 Pro",
    "stock",
    "store",
    "2000 N Shoreline Blvd",
    "Mountain View",
]


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_chat() -> None:
    chat = function_calling_chat.generate_function_call_chat()

    assert chat
    assert chat.history
    assert any(x in str(chat.history) for x in summaries_expected)
