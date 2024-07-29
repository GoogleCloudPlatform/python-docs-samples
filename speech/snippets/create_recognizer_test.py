# Copyright 2022 Google LLC
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
from uuid import uuid4

from google.api_core.retry import Retry
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

import pytest

import create_recognizer


def delete_recognizer(name: str) -> None:
    client = SpeechClient()
    request = cloud_speech.DeleteRecognizerRequest(name=name)
    client.delete_recognizer(request=request)


@Retry()
def test_create_recognizer(
    capsys: pytest.CaptureFixture, request: pytest.FixtureRequest
) -> None:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    recognizer_id = "recognizer-" + str(uuid4())

    def cleanup():
        delete_recognizer(
            f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"
        )

    request.addfinalizer(cleanup)

    recognizer = create_recognizer.create_recognizer(project_id, recognizer_id)

    assert recognizer_id in recognizer.name
