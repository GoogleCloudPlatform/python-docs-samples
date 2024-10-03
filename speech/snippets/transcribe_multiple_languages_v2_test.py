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

from google.api_core.retry import Retry

import transcribe_multiple_languages_v2

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_transcribe_multiple_languages_v2() -> None:
    response = transcribe_multiple_languages_v2.transcribe_multiple_languages_v2(
        os.path.join(RESOURCES, "audio.wav"),
        ["en-US", "fr-FR"],
    )

    assert re.search(
        r"how old is the Brooklyn Bridge",
        response.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )
