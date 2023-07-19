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

import extraction


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
_LOCATION = "us-central1"


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_extractive_question_answering() -> None:
    content = extraction.extractive_question_answering(
        temperature=0, project_id=_PROJECT_ID, location=_LOCATION
    )
    assert content == "Reduced moist tropical vegetation cover in the basin."
