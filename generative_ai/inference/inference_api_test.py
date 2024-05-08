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

import non_stream_multimodality_basic
import non_stream_text_basic
import stream_multimodality_basic
import stream_text_basic


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"
MODEL_ID = "gemini-1.5-pro-preview-0409"


def test_non_stream_text_basic() -> None:
    response = non_stream_text_basic.generate_content(PROJECT_ID, REGION, MODEL_ID)
    assert response


def test_non_stream_multi_modality_basic() -> None:
    response = non_stream_multimodality_basic.generate_content(
        PROJECT_ID, REGION, MODEL_ID
    )
    assert response


def test_stream_text_basic() -> None:
    responses = stream_text_basic.generate_content(PROJECT_ID, REGION, MODEL_ID)
    assert responses


def test_stream_multi_modality_basic() -> None:
    responses = stream_multimodality_basic.generate_content(
        PROJECT_ID, REGION, MODEL_ID
    )
    assert responses
