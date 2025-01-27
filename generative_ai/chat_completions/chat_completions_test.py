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

import chat_completions_authentication
import chat_completions_credentials_refresher
import chat_completions_non_streaming_image
import chat_completions_non_streaming_text
import chat_completions_non_streaming_text_self_deployed
import chat_completions_streaming_image
import chat_completions_streaming_text
import chat_completions_streaming_text_self_deployed


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
SELF_HOSTED_MODEL_ID = "google/gemma-2-9b-it"
ENDPOINT_ID = "6714120476014149632"


def test_authentication() -> None:
    response = chat_completions_authentication.generate_text(PROJECT_ID, LOCATION)
    assert response


def test_streaming_text() -> None:
    response = chat_completions_streaming_text.generate_text(PROJECT_ID, LOCATION)
    assert response


def test_non_streaming_text() -> None:
    response = chat_completions_non_streaming_text.generate_text(PROJECT_ID, LOCATION)
    assert response


def test_streaming_image() -> None:
    response = chat_completions_streaming_image.generate_text(PROJECT_ID, LOCATION)
    assert response


def test_non_streaming_image() -> None:
    response = chat_completions_non_streaming_image.generate_text(PROJECT_ID, LOCATION)
    assert response


def test_credentials_refresher() -> None:
    response = chat_completions_credentials_refresher.generate_text(
        PROJECT_ID, LOCATION
    )
    assert response


def test_streaming_text_self_deployed() -> None:
    response = chat_completions_streaming_text_self_deployed.generate_text(
        PROJECT_ID, LOCATION, SELF_HOSTED_MODEL_ID, ENDPOINT_ID
    )
    assert response


def test_non_streaming_text_self_deployed() -> None:
    response = chat_completions_non_streaming_text_self_deployed.generate_text(
        PROJECT_ID, LOCATION, SELF_HOSTED_MODEL_ID, ENDPOINT_ID
    )
    assert response
