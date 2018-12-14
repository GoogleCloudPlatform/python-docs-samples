# Copyright 2018, Google LLC
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

from detect_intent_with_model_selection import \
    detect_intent_with_model_selection

DIRNAME = os.path.realpath(os.path.dirname(__file__))
PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'fake_session_for_testing'
AUDIOS = [
    '{0}/resources/book_a_room.wav'.format(DIRNAME),
    '{0}/resources/mountain_view.wav'.format(DIRNAME),
    '{0}/resources/today.wav'.format(DIRNAME),
]


def test_detect_intent_audio_with_model_selection(capsys):
    for audio_file_path in AUDIOS:
        detect_intent_with_model_selection(PROJECT_ID, SESSION_ID,
                                           audio_file_path, 'en-US')
    out, _ = capsys.readouterr()

    assert 'Fulfillment text: What time will the meeting start?' in out
