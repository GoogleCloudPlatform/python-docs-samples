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


# [START hybrid_imports]
# Imports the Google Cloud client libraries
from google.cloud import translate_v3beta1 as translate
from google.cloud import vision
from google.cloud import texttospeech

import io
# [END hybrid_imports]

# [START hybrid_vision]
def pic_to_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # For dense text, use document_text_detection
    # For less dense text, use text_detection
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text
    return text
    # [END hybrid_vision]


# [START hybrid_translate]
def translate_text(text, prev_lang, new_lang, project_id, glossary_name):
    """Translates text to a given language using a glossary"""
    client = translate.TranslationServiceClient()

    project_id = 'ec-gcp'
    glossary_name = 'bistro-glossary'
    location = 'us-central1'  # The location of the glossary

    glossary = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_name)
    print(glossary)

    glossary_config = translate.types.TranslateTextGlossaryConfig(
        glossary=glossary)

    resource = client.location_path(project_id, location)

    result = client.translate_text(
        parent=resource,
        contents=[text],
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code=prev_lang,
        target_language_code=new_lang,
        glossary_config=glossary_config)

    # Return translated text
    return result.glossary_translations[0].translated_text
    # [END hybrid_translate]


# [START hybrid_create_glossary]
def create_glossary(languages, project_id, glossary_name, glossary_uri):

    # Instantiate a client
    client = translate.TranslationServiceClient()

    # Set information to access 
    glossary_uri = 'gs://cloud-samples-data/translation/bistro_glossary.csv'
    location = 'us-central1'

    # Set languages that the glossary uses
    # Here, the glossary includes French and English
    languages = ['fr', 'en']

    # Set glossary resource name
    name = client.glossary_path(
        project_id,
        location,
        glossary_name)

    # Set language codes
    language_codes_set = translate.types.Glossary.LanguageCodesSet(
        language_codes=languages)

    # todo
    gcs_source = translate.types.GcsSource(
        input_uri=glossary_uri)

    # todo
    input_config = translate.types.GlossaryInputConfig(
        gcs_source=gcs_source)

    # Set glossary resource information
    glossary = translate.types.Glossary(
        name=name,
        language_codes_set=language_codes_set,
        input_config=input_config)

    parent = client.location_path(project_id, location)

    # Create glossary resource
    operation = client.create_glossary(parent=parent, glossary=glossary)

    return operation.result(timeout=90)

def delete_glossary(project_id, glossary_id):
    # [START translate_delete_glossary_beta]
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()

    parent = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_id)

    operation = client.delete_glossary(parent)
    result = operation.result(timeout=90)
    print('Deleted: {}'.format(result.name))


# [START hybrid_tts]
def text_to_speech(text, outfile):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    # Selects the type of audio file to return
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # Writes the synthetic audio to the output file.
    with open(outfile, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + outfile)
    # [END hybrid_tts]


# [START hybrid_integration]
def main():
    # Photo from which to extract text
    infile = "resources/example.JPG" 
    # Name of file that will hold synthetic speech
    outfile = "resources/example.mp3" 

    #delete_glossary('ec-gcp', 'test-glossary')   
    #create_glossary(['fr', 'en'], 'ec-gcp', 'test', 'gs://cloud-samples-data/translation/bistro_glossary.csv')
    print translate_text('je mange du chevre. j\'aime le bouillabaisse et creme brulee et frites', 'fr', 'en', 'ec-gcp', 'bistro-glossary')
"""
    text_to_translate = pic_to_text(infile)
    text_to_speak = translate_text(text_to_translate)
    text_to_speech(text_to_speak, outfile)
    # [END hybrid_integration]
"""


if __name__ == '__main__':
    main()
