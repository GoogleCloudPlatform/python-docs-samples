# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.api_core.retry import Retry
from google.cloud import speech_v1p1beta1 as speech
import pytest

import speech_model_adaptation_beta


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AUDIO_URI = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
client = speech.AdaptationClient()


@Retry()
def test_model_adaptation_beta(
    custom_class_id: str, phrase_set_id: str, capsys: pytest.CaptureFixture
) -> None:
    class_id = custom_class_id
    phrase_id = phrase_set_id
    transcript = speech_model_adaptation_beta.transcribe_with_model_adaptation(
        AUDIO_URI, class_id, phrase_id
    )
    assert "how old is the Brooklyn Bridge" in transcript


@pytest.fixture
def custom_class_id() -> str:
    # The custom class id can't be too long
    custom_class_id = f"customClassId{str(uuid.uuid4())[:8]}"
    yield custom_class_id
    # clean up resources
    CLASS_PARENT = (
        f"projects/{PROJECT_ID}/locations/global/customClasses/{custom_class_id}"
    )
    client.delete_custom_class(name=CLASS_PARENT)


@pytest.fixture
def phrase_set_id() -> str:
    # The phrase set id can't be too long
    phrase_set_id = f"phraseSetId{str(uuid.uuid4())[:8]}"
    yield phrase_set_id
    # clean up resources
    PHRASE_PARENT = f"projects/{PROJECT_ID}/locations/global/phraseSets/{phrase_set_id}"
    client.delete_phrase_set(name=PHRASE_PARENT)
