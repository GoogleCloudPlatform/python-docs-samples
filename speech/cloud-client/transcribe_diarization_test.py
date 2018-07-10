# Copyright 2018, Google, LLC.
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
import re

import transcribe_diarization

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
OUTPUT1 = 'OK Google stream stranger things from Netflix to my TV'
OUTPUT2 = 'Speaker Tag'


def test_transcribe_diarization(capsys):
    transcribe_diarization.speech_transcribe_diarization(
        os.path.join(RESOURCES, 'Google_Gnome.wav'))
    out, err = capsys.readouterr()

    assert re.search(OUTPUT1, out, re.DOTALL | re.I)
    assert re.search(OUTPUT2, out, re.DOTALL | re.I)


def test_transcribe_diarization_gcs(capsys):
    transcribe_diarization.speech_transcribe_diarization_gcs(
        'gs://cloud-samples-tests/speech/Google_Gnome.wav')
    out, err = capsys.readouterr()

    assert re.search(OUTPUT1, out, re.DOTALL | re.I)
    assert re.search(OUTPUT2, out, re.DOTALL | re.I)
