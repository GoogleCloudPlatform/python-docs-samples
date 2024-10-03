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

from flaky import flaky

from google.api_core.retry import Retry

import transcribe_multichannel_v2

_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
@flaky(max_runs=3, min_passes=1)
def test_transcribe_multichannel_v2() -> None:
    response = transcribe_multichannel_v2.transcribe_multichannel_v2(
        os.path.join(_RESOURCES, "two_channel_16k.wav")
    )

    assert re.search(
        r"saving account",
        response.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )
    assert response.results[0].channel_tag == 1

    assert re.search(
        r"debit card number",
        response.results[1].alternatives[0].transcript,
        re.DOTALL | re.I,
    )
    assert response.results[1].channel_tag == 2
