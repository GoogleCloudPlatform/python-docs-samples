# Copyright 2017 Google LLC

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

from __future__ import absolute_import

import os
import uuid

from detect_intent_audio import detect_intent_audio

DIRNAME = os.path.realpath(os.path.dirname(__file__))
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
SESSION_ID = "test_{}".format(uuid.uuid4())
AUDIOS = [
    "{0}/resources/book_a_room.wav".format(DIRNAME),
    "{0}/resources/mountain_view.wav".format(DIRNAME),
    "{0}/resources/today.wav".format(DIRNAME),
]


def test_detect_intent_audio(capsys):
    for audio_file_path in AUDIOS:
        detect_intent_audio(PROJECT_ID, SESSION_ID, audio_file_path, "en-US")
    out, _ = capsys.readouterr()

    assert "Fulfillment text: What time will the meeting start?" in out
