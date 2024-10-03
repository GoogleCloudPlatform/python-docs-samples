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
import re
from uuid import uuid4

from google.api_core.retry import Retry
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

import pytest

import transcribe_reuse_recognizer

_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_recognizer(project_id: str, recognizer_id: str) -> None:
    client = SpeechClient()
    request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{project_id}/locations/global",
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            default_recognition_config=cloud_speech.RecognitionConfig(
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                language_codes=["en-US"],
                model="long",
            ),
        ),
    )
    client.create_recognizer(request=request)


def delete_recognizer(project_id: str, recognizer_id: str) -> None:
    client = SpeechClient()
    request = cloud_speech.DeleteRecognizerRequest(
        name=f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"
    )
    client.delete_recognizer(request=request)


@Retry()
def test_transcribe_reuse_recognizer(
    capsys: pytest.CaptureFixture, request: pytest.FixtureRequest
) -> None:
    recognizer_id = "recognizer-" + str(uuid4())

    def cleanup() -> None:
        delete_recognizer(PROJECT_ID, recognizer_id)

    request.addfinalizer(cleanup)

    create_recognizer(PROJECT_ID, recognizer_id)

    response = transcribe_reuse_recognizer.transcribe_reuse_recognizer(
        os.path.join(_RESOURCES, "audio.wav"),
        recognizer_id,
    )

    assert re.search(
        r"how old is the Brooklyn Bridge",
        response.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )
