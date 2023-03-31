# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.api_core.retry import Retry

import speech_quickstart_beta


@Retry()
def test_quickstart_beta():
    response = speech_quickstart_beta.sample_recognize(
        "gs://cloud-samples-data/speech/brooklyn_bridge.mp3"
    )
    assert "brooklyn" in response.results[0].alternatives[0].transcript.lower()
