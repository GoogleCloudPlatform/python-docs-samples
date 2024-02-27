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

import function_calling_chat


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
_LOCATION = "us-central1"


summaries_expected = [
    "Pixel 8 Pro",
    "stock",
    "SKU",
    "store",
    "Mountain View",
    "address",
    "2000 N Shoreline Blvd",
]

responses_expected = [
    "candidates",
    "content",
    "role",
    "model",
    "parts",
    "GA04834-US",
    "2000 N Shoreline Blvd",
]

responses_fc_expected = [
    "function_call",
    "get_product_sku",
    "get_store_location",
    "args",
    "fields",
    "product_name",
    "Pixel 8 Pro",
    "location",
    "Mountain View",
]


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_chat() -> None:
    (
        _,
        summaries,
        responses,
        responses_fc,
    ) = function_calling_chat.generate_function_call_chat(
        project_id=_PROJECT_ID,
        location=_LOCATION,
    )
    assert all(x in str(summaries) for x in summaries_expected)
    assert all(x in str(responses) for x in responses_expected)
    assert all(x in str(responses_fc) for x in responses_fc_expected)
