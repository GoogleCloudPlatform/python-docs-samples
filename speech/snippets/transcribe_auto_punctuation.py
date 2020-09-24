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

"""Google Cloud Speech API sample that demonstrates auto punctuation
and recognition metadata.

Example usage:
    python transcribe_auto_punctuation.py resources/commercial_mono.wav
"""

import argparse
import io


def transcribe_file_with_auto_punctuation(path):
    """Transcribe the given audio file with auto punctuation enabled."""
    # [START speech_transcribe_auto_punctuation]
    from google.cloud import speech

    client = speech.SpeechClient()

    # path = 'resources/commercial_mono.wav'
    with io.open(path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
    )

    response = client.recognize(request={"config": config, "audio": audio})

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print("Transcript: {}".format(alternative.transcript))
    # [END speech_transcribe_auto_punctuation]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="File to stream to the API")

    args = parser.parse_args()

    transcribe_file_with_auto_punctuation(args.path)
