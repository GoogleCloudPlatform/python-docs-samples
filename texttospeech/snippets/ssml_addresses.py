#!/usr/bin/env python
# Copyright 2018 Google LLC
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
#
# All Rights Reserved.


# [START tts_ssml_address_imports]
import html

from google.cloud import texttospeech

# [END tts_ssml_address_imports]


# [START tts_ssml_address_audio]
def ssml_to_audio(ssml_text, outfile):
    # Generates SSML text from plaintext.
    #
    # Given a string of SSML text and an output file name, this function
    # calls the Text-to-Speech API. The API returns a synthetic audio
    # version of the text, formatted according to the SSML commands. This
    # function saves the synthetic audio to the designated output file.
    #
    # Args:
    # ssml_text: string of SSML text
    # outfile: string name of file under which to save audio output
    #
    # Returns:
    # nothing

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Writes the synthetic audio to the output file.
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)
    # [END tts_ssml_address_audio]


# [START tts_ssml_address_ssml]
def text_to_ssml(inputfile):
    # Generates SSML text from plaintext.
    # Given an input filename, this function converts the contents of the text
    # file into a string of formatted SSML text. This function formats the SSML
    # string so that, when synthesized, the synthetic audio will pause for two
    # seconds between each line of the text file. This function also handles
    # special text characters which might interfere with SSML commands.
    #
    # Args:
    # inputfile: string name of plaintext file
    #
    # Returns:
    # A string of SSML text based on plaintext input

    # Parses lines of input file
    with open(inputfile, "r") as f:
        raw_lines = f.read()

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )

    # Return the concatenated string of ssml script
    return ssml


# [END tts_ssml_address_ssml]


# [START tts_ssml_address_test]
def main():
    # test example address file
    plaintext = "resources/example.txt"
    ssml_text = text_to_ssml(plaintext)
    ssml_to_audio(ssml_text, "resources/example.mp3")
    # [END tts_ssml_address_test]


if __name__ == "__main__":
    main()
