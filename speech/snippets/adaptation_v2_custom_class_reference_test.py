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
import re
from uuid import uuid4

from google.api_core.retry import Retry
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

import adaptation_v2_custom_class_reference

_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


def delete_phrase_set(name: str) -> None:
    client = SpeechClient()
    request = cloud_speech.DeletePhraseSetRequest(name=name)
    client.delete_phrase_set(request=request)


def delete_custom_class(name: str) -> None:
    client = SpeechClient()
    request = cloud_speech.DeleteCustomClassRequest(name=name)
    client.delete_custom_class(request=request)


@Retry()
def test_adaptation_v2_custom_class_reference() -> None:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    phrase_set_id = "phrase-set-" + str(uuid4())
    custom_class_id = "custom-class-" + str(uuid4())
    response = (
        adaptation_v2_custom_class_reference.adaptation_v2_custom_class_reference(
            project_id,
            phrase_set_id,
            custom_class_id,
            os.path.join(_RESOURCES, "fair.wav"),
        )
    )

    assert re.search(
        r"the word is fare",
        response.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )

    delete_phrase_set(
        f"projects/{project_id}/locations/global/phraseSets/{phrase_set_id}"
    )

    delete_custom_class(
        f"projects/{project_id}/locations/global/customClasses/{custom_class_id}"
    )
