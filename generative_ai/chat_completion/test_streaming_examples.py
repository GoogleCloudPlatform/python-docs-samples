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

import non_streaming_image
import non_streaming_text
import streaming_image
import streaming_text

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"


def test_streaming_text() -> None:
    response = streaming_text.example(PROJECT_ID, REGION)
    assert type(response) is str, "Expected text response"
    assert len(response) > 0, "Expected text response"


def test_non_streaming_text() -> None:
    response = streaming_image.example(PROJECT_ID, REGION)
    assert type(response) is str, "Expected text response"
    assert len(response) > 0, "Expected text response"


def test_streaming_image() -> None:
    response = non_streaming_text.example(PROJECT_ID, REGION)
    assert type(response) is str, "Expected text response"
    assert len(response) > 0, "Expected text response"


def test_non_streaming_image() -> None:
    response = non_streaming_image.example(PROJECT_ID, REGION)
    assert type(response) is str, "Expected text response"
    assert len(response) > 0, "Expected text response"
