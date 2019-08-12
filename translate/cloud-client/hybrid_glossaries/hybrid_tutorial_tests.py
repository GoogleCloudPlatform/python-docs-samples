# Copyright 2019 Google LLC. All Rights Reserved.
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

from google.cloud import translate_v3beta1 as translate

from hybrid_tutorial import pic_to_text
from hybrid_tutorial import create_glossary
from hybrid_tutorial import translate_text
from hybrid_tutorial import text_to_speech

import filecmp
import os

PROJECT_ID = os.environ['GCLOUD_PROJECT']


# [START translate_hybrid_glossary_delete]
def delete_glossary(project_id, glossary_name):
    # Deletes a GCP glossary resource
    #
    # ARGS
    # project_id: GCP project id
    # glossary_name: name you gave your project's glossary
    #   resource when you created it
    #
    # RETURNS
    # nothing

    # Designates the data center location that you want to use
    location = 'us-central1'

    # Instantiates a client
    client = translate.TranslationServiceClient()

    resource = client.glossary_path(
        project_id,
        location,
        glossary_name)

    operation = client.delete_glossary(resource)
    result = operation.result(timeout=90)

    print('Deleted: {}'.format(result.name))
    # [END translate_hybrid_glossary_delete]


# VISION TESTS


def test_vision_standard_format():

    expected_text = 'This is\na test!\n'
    alt_expected_text = 'This\nis\na test!\n'

    # Generate text using Vision API
    text = pic_to_text('resources/standard_format.jpeg')

    assert (text == expected_text) or (text == alt_expected_text)


def test_vision_non_standard_format():

    # Generate text
    text = pic_to_text('resources/non_standard_format.png')

    # Read expected text
    with open('resources/non_standard_format.txt') as f:
        expected_text = f.read()

    assert text == expected_text


# TRANSLATE TESTS


def test_create_and_delete_glossary():
    languages = ['fr', 'en']
    glossary_name = 'test-glossary'
    glossary_uri = 'gs://cloud-samples-data/translation/bistro_glossary.csv'

    # create_glossary will raise an exception if creation fails
    create_glossary(languages, PROJECT_ID, glossary_name,
                    glossary_uri)

    # Delete glossary so that future tests will pass
    # delete_glossary will raise an exception if deletion fails
    delete_glossary(PROJECT_ID, glossary_name)


def test_translate_standard():

    expected_text = 'Hello'

    text = translate_text('Bonjour', 'fr', 'en', PROJECT_ID,
                          'bistro-glossary')

    assert text == expected_text


def test_translate_glossary():

    expected_text = 'I eat goat cheese'
    input_text = 'Je mange du chevre'

    text = translate_text(input_text, 'fr', 'en', PROJECT_ID,
                          'bistro-glossary')

    assert text == expected_text


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
    assert 'Audio content written to file ' + outfile in out

    # Delete test file
    os.remove(outfile)
