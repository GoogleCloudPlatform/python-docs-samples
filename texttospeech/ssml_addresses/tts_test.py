# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tts import text_to_ssml
from tts import ssml_to_audio

import filecmp
import os


def test_text_to_ssml(capsys):

    # Read expected SSML output from resources
    with open('resources/example.ssml', 'r') as f:
        expected_ssml = f.read()

    # Assert plaintext converted to SSML
    input_text = 'resources/example.txt'
    tested_ssml = text_to_ssml(input_text)
    assert expected_ssml == tested_ssml


def test_ssml_to_audio(capsys):

    # Read SSML input from resources
    with open('resources/example.ssml', 'r') as f:
        input_ssml = f.read()

    # Assert audio file generated
    ssml_to_audio(input_ssml, 'test_example.mp3')
    assert os.path.isfile('test_example.mp3')

    # Assert audio file generated correctly
    assert filecmp.cmp('test_example.mp3',
                       'resources/expected_example.mp3',
                       shallow=True)
    out, err = capsys.readouterr()

    # Delete test file
    os.remove("test_example.mp3")

    # Assert success message printed
    assert "Audio content written to file test_example.mp3" in out
