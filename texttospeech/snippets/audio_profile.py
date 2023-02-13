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

"""Google Cloud Text-To-Speech API sample application for audio profile.

Example usage:
    python audio_profile.py --text "hello" --effects_profile_id
        "telephony-class-application" --output "output.mp3"
"""

import argparse


# [START tts_synthesize_text_audio_profile]
# [START tts_synthesize_text_audio_profile_beta]
def synthesize_text_with_audio_profile(text, output, effects_profile_id):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(language_code="en-US")

    # Note: you can pass in multiple effects_profile_id. They will be applied
    # in the same order they are provided.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=[effects_profile_id],
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "%s"' % output)


# [END tts_synthesize_text_audio_profile_beta]
# [END tts_synthesize_text_audio_profile]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--output", help="The output mp3 file.")
    parser.add_argument("--text", help="The text from which to synthesize speech.")
    parser.add_argument(
        "--effects_profile_id", help="The audio effects profile id to be applied."
    )

    args = parser.parse_args()

    synthesize_text_with_audio_profile(args.text, args.output, args.effects_profile_id)
