#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample that demonstrates how to select the model
used for speech recognition.

Example usage:
    python transcribe_model_selection.py \
        resources/Google_Gnome.wav --model video
    python transcribe_model_selection.py \
        gs://cloud-samples-tests/speech/Google_Gnome.wav --model video
"""

import argparse


# [START speech_transcribe_model_selection]
def transcribe_model_selection(speech_file, model):
    """Transcribe the given audio file synchronously with
    the selected model."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print("Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_model_selection]


# [START speech_transcribe_model_selection_gcs]
def transcribe_model_selection_gcs(gcs_uri, model):
    """Transcribe the given audio file asynchronously with
    the selected model."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print("Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_model_selection_gcs]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="File or GCS path for audio file to be recognized")
    parser.add_argument(
        "--model",
        help="The speech recognition model to use",
        choices=["command_and_search", "phone_call", "video", "default"],
        default="default",
    )

    args = parser.parse_args()

    if args.path.startswith("gs://"):
        transcribe_model_selection_gcs(args.path, args.model)
    else:
        transcribe_model_selection(args.path, args.model)
