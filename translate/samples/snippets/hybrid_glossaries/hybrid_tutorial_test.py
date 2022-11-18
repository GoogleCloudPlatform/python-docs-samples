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

import os
import sys
import uuid

from hybrid_tutorial import create_glossary
from hybrid_tutorial import pic_to_text
from hybrid_tutorial import text_to_speech
from hybrid_tutorial import translate_text


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


# VISION TESTS


def test_vision_standard_format():
    # Generate text using Vision API
    text = pic_to_text('resources/standard_format.jpeg')

    assert len(text) > 0


# TRANSLATE TESTS


def test_create_and_delete_glossary():
    sys.path.insert(1, "../")
    from translate_v3_delete_glossary import delete_glossary

    languages = ["fr", "en"]
    glossary_name = f"test-glossary-{uuid.uuid4()}"
    glossary_uri = "gs://cloud-samples-data/translation/bistro_glossary.csv"

    # create_glossary will raise an exception if creation fails
    create_glossary(languages, PROJECT_ID, glossary_name, glossary_uri)

    # Delete glossary so that future tests will pass
    # delete_glossary will raise an exception if deletion fails
    delete_glossary(PROJECT_ID, glossary_name)


def test_translate_standard():

    expected_text = "Hello"

    # attempt to create glossary, fails if it already exists
    languages = ["fr", "en"]
    glossary_name = "bistro-glossary"
    glossary_uri = f"gs://cloud-samples-data/translation/{glossary_name}.csv"
    create_glossary(languages, PROJECT_ID, glossary_name, glossary_uri)

    text = translate_text("Bonjour", "fr", "en", PROJECT_ID, "bistro-glossary")

    assert text == expected_text


def test_translate_glossary():

    expected_text = "I eat goat cheese"
    input_text = "Je mange du chevre"

    # attempt to create glossary, fails if it already exists
    languages = ["fr", "en"]
    glossary_name = "bistro-glossary"
    glossary_uri = f"gs://cloud-samples-data/translation/{glossary_name}.csv"
    create_glossary(languages, PROJECT_ID, glossary_name, glossary_uri)

    text = translate_text(input_text, "fr", "en", PROJECT_ID, "bistro-glossary")

    assert text == expected_text


# TEXT-TO-SPEECH TESTS


def test_tts_standard(capsys):
    outfile = "resources/test_standard_text.mp3"
    text = "this is\na test!"

    text_to_speech(text, outfile)

    # Assert audio file generated
    assert os.path.isfile(outfile)
    out, err = capsys.readouterr()

    # Assert success message printed
    assert "Audio content written to file " + outfile in out

    # Delete test file
    os.remove(outfile)
