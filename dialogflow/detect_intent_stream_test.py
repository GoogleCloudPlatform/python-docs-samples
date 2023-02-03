# Copyright 2017, Google LLC

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

from detect_intent_stream import detect_intent_stream

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
SESSION_ID = "test_{}".format(uuid.uuid4())
AUDIO_FILE_PATH = "{0}/resources/book_a_room.wav".format(
    os.path.realpath(os.path.dirname(__file__)),
)


def test_detect_intent_stream(capsys):
    detect_intent_stream(PROJECT_ID, SESSION_ID, AUDIO_FILE_PATH, "en-US")
    out, _ = capsys.readouterr()

    assert "Intermediate transcript:" in out
    assert "Fulfillment text:" in out
