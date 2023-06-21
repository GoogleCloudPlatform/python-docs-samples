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

import pytest  # noqa: I100

import hybrid_tutorial  # noqa: I100


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


# VISION TESTS


def test_vision_standard_format() -> None:
    # Generate text using Vision API
    text = hybrid_tutorial.pic_to_text("resources/standard_format.jpeg")

    assert len(text) > 0


# TRANSLATE TESTS


def test_create_and_delete_glossary() -> None:
    sys.path.insert(1, "../")
    from google.cloud import translate_v3 as translate

    languages = ["fr", "en"]
    glossary_name = f"test-glossary-{uuid.uuid4()}"
    glossary_uri = "gs://cloud-samples-data/translation/bistro_glossary.csv"

    # create_glossary will raise an exception if creation fails
    created_glossary_name = hybrid_tutorial.create_glossary(
        languages, PROJECT_ID, glossary_name, glossary_uri
    )

    # Delete glossary so that future tests will pass
    # delete_glossary will raise an exception if deletion fails
    client = translate.TranslationServiceClient()

    name = client.glossary_path(PROJECT_ID, "us-central1", created_glossary_name)

    operation = client.delete_glossary(name=name)
    result = operation.result(timeout=180)
    assert created_glossary_name in result.name
    print(f"Deleted: {result.name}")


def test_translate_standard() -> None:
    expected_text = "Good morning"

    # attempt to create glossary, fails if it already exists
    languages = ["fr", "en"]
    glossary_name = "bistro-glossary"
    glossary_uri = f"gs://cloud-samples-data/translation/{glossary_name}.csv"
    created_glossary_name = hybrid_tutorial.create_glossary(
        languages, PROJECT_ID, glossary_name, glossary_uri
    )

    text = hybrid_tutorial.translate_text(
        "Bonjour", "fr", "en", PROJECT_ID, created_glossary_name
    )

    assert text == expected_text


def test_translate_glossary() -> None:
    expected_text = "I eat goat cheese"
    input_text = "Je mange du chevre"

    # attempt to create glossary, fails if it already exists
    languages = ["fr", "en"]
    glossary_name = "bistro-glossary"
    glossary_uri = f"gs://cloud-samples-data/translation/{glossary_name}.csv"
    created_glossary_name = hybrid_tutorial.create_glossary(
        languages, PROJECT_ID, glossary_name, glossary_uri
    )

    text = hybrid_tutorial.translate_text(
        input_text, "fr", "en", PROJECT_ID, created_glossary_name
    )

    assert text == expected_text


# TEXT-TO-SPEECH TESTS


def test_tts_standard(capsys: pytest.LogCaptureFixture) -> None:
    outfile = "resources/test_standard_text.mp3"
    text = "this is\na test!"

    generated_outfile = hybrid_tutorial.text_to_speech(text, outfile)

    # Assert audio file generated
    assert os.path.isfile(generated_outfile)
    out, err = capsys.readouterr()

    # Assert success message printed
    assert "Audio content written to file " + generated_outfile in out

    # Delete test file
    os.remove(outfile)
