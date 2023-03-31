# Copyright 2018 Google LLC
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

import os

import transcribe_enhanced_model

from google.api_core.retry import Retry

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_transcribe_file_with_enhanced_model(capsys):
    transcribe_enhanced_model.transcribe_file_with_enhanced_model(
        "resources/commercial_mono.wav"
    )
    out, _ = capsys.readouterr()

    assert "Chrome" in out
