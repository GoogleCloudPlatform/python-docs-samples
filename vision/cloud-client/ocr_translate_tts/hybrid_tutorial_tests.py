# Copyright 2018 Google Inc. All Rights Reserved.
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

from hybrid_tutorial import pic_to_text
from hybrid_tutorial import translate_text
from hybrid_tutorial import text_to_speech

import filecmp
import os


# VISION TESTS


def test_vision_standard_format():

    # Generate text
    text = pic_to_text("resources/standard_format.JPG")

    # Read expected text
    with open("resources/standard_format.txt") as f:
        expected_text = f.read()
    
    assert text == expected_text

def test_vision_non_standard_format():

    # Generate text
    text = pic_to_text("resources/non_standard_format.png")

    # Read expected text
    with open("resources/non_standard_format.txt") as f:
        expected_text = f.read()
    
    assert text == expected_text


"""
def test_vision_special_chars():

    # Generate text
    text = pic_to_text("resources/special_chars.jpg")

    # Read expected text
    with open("resources/standard_format.txt") as f:
        expected_text = f.read()
    
    assert text is expected_text
"""

# TRANSLATE TESTS


def test_translate_standard():

    text = translate_text("hello", "en", "blah")
    expected_text = "hello"
    assert text == expected_text

def test_translate_glossary():
    return

# TEXT-TO-SPEECH TESTS


def test_tts_standard(capsys):
    outfile = 'resources/test_standard_text.mp3'
    expected_outfile = 'resources/expected_standard_text.mp3'
    textfile = 'resources/standard_format.txt'

    with open(textfile, 'r') as f:
        text = f.read()

    text_to_speech(text, outfile)

    # Assert audio file generated
    assert os.path.isfile(outfile)

    # Assert audio file generated correctly
    assert filecmp.cmp(outfile,
                       expected_outfile,
                       shallow=True)

    out, err = capsys.readouterr()

    # Assert success message printed
    assert "Audio content written to file " + outfile in out

    # Delete test file
    os.remove(outfile)

def test_tts_special_chars():
    
    return
