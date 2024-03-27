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

"""Google Cloud Text-To-Speech API sample application .

Example usage:
    python synthesize_long_audio.py --text "hello"
"""

import argparse


# [START tts_synthesize_long_audio]
def synthesize_long_audio(parent, text, output_gcs_uri):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    
    client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = client.synthesize_long_audio(
        request={"parent": parent, "input": input_text, "voice": voice, "audio_config": audio_config, "output_gcs_uri": output_gcs_uri}
    )
    # Wait for the LRO to finish.
    while not response.done:
        sleep(5)

    return response


# [END tts_synthesize_long_audio]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--text", help="The text from which to synthesize speech.")
    parser.add_argument("--output_gcs_uri", help="The GCS path to write the audio to e.g. gs://my-bucket/output.wav.")
    parser.add_argument("--parent", help="The parent path to run the LRO to e.g. projects/<my-project>/locations/global")

    args = parser.parse_args()
    synthesize_text(parent, args.text, args.output_gcs_uri)
