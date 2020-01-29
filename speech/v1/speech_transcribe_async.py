# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "speech_transcribe_async")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Transcribe Audio File using Long Running Operation (Local File) (LRO)
#   description: Transcribe a long audio file using asynchronous speech recognition
#   usage: python3 samples/v1/speech_transcribe_async.py [--local_file_path "resources/brooklyn_bridge.raw"]

# [START speech_transcribe_async]
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io


def sample_long_running_recognize(local_file_path):
    """
    Transcribe a long audio file using asynchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_async]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local_file_path", type=str, default="resources/brooklyn_bridge.raw"
    )
    args = parser.parse_args()

    sample_long_running_recognize(args.local_file_path)


if __name__ == "__main__":
    main()
