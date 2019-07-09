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
import sys


def test_text_to_ssml():
    # Tests text_to_ssml() function
    # Args: none
    # Returns: array of 2 ssml strings

    # Assert non-special characters converted to SSML
    input_chars = 'normal_chars.txt'
    tested_chars = text_to_ssml(input_chars)
    expected_chars = '<speak>This is a normal test.\n' \
                     '<break time="2s"/>Hopefully it passes!\n' \
                     '<break time="2s"/>:)<break time="2s"/></speak>'
    assert tested_chars == expected_chars

    # Assert special characters converted to SSML
    input_special_chars = 'special_chars.txt'
    tested_special_chars = text_to_ssml(input_special_chars)
    expected_special_chars = '<speak>&lt;&amp;&gt;\n<' \
                             'break time="2s"/>&gt;&gt;\n' \
                             '<break time="2s"/>&amp;' \
                             '<break time="2s"/></speak>'
    assert tested_special_chars == expected_special_chars

    # Assert that nothing returned if given nonexistent input
    non_existent_input = text_to_ssml('mysteryfile.txt')
    assert non_existent_input is None


def test_ssml_to_audio():
    # Tests ssml_to_audio() function
    # Args: ssml = array of 2 ssml strings
    # Returns: none

    non_special_ssml = '<speak>This is a normal test.\n' \
                       '<break time="2s"/>Hopefully it passes!\n' \
                       '<break time="2s"/>:)<break time="2s"/></speak>'
    special_ssml = '<speak>&lt;&amp;&gt;\n<' \
                   'break time="2s"/>&gt;&gt;\n' \
                   '<break time="2s"/>&amp;<break time="2s"/></speak>'

    # Assert audio file of non-special characters generated
    ssml_to_audio(non_special_ssml, 'test_non_special.mp3')
    assert os.path.isfile('test_non_special.mp3')

    # Assert audio file of non-special characters generated correctly
    assert filecmp.cmp('test_non_special.mp3', 'expected_non_special.mp3',
            shallow=True)

    # Assert audio file of special characters generated
    ssml_to_audio(special_ssml, 'test_special.mp3')
    assert os.path.isfile('test_special.mp3')

    # Assert audio file of special characters generated correctly
    assert filecmp.cmp('test_special.mp3', 'expected_special.mp3',
            shallow=True)

    # Assert that no mp3 file generated if given empty SSML input
    # NOTE to work correctly, directory must not already contain a file
    # named 'out3.mp3'
    ssml_to_audio(None, 'non_existent_input.mp3')
    assert os.path.isfile('non_existent_input.mp3') is False


def suppressPrint():
    # Suppresses printing; helper function
    # Args: none
    # Returns: none

    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    # Enables printing; helper function
    # Args: None
    # Returns: None

    sys.stdout = sys.__stdout__


if __name__ == '__main__':

    # Suppress printing while testing
    suppressPrint()

    # Test text_to_ssml()
    test_text_to_ssml()

    # Test ssml_to_audio()
    test_ssml_to_audio()

    # Restore printing
    enablePrint()

    # Print success if achieved
    print("All tests passed!")
