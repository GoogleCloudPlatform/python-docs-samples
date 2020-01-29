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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_auto_punctuation_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Getting punctuation in results (Local File) (Beta)
#   description: Transcribe a short audio file with punctuation
#   usage: python3 samples/v1p1beta1/speech_transcribe_auto_punctuation_beta.py [--local_file_path "resources/commercial_mono.wav"]

# [START speech_transcribe_auto_punctuation_beta]
from google.cloud import speech_v1p1beta1
import io


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file with punctuation

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/commercial_mono.wav'

    # When enabled, trascription results may include punctuation
    # (available for select languages).
    enable_automatic_punctuation = True

    # The language of the supplied audio. Even though additional languages are
    # provided by alternative_language_codes, a primary language is still required.
    language_code = "en-US"
    config = {
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "language_code": language_code,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_auto_punctuation_beta]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local_file_path", type=str, default="resources/commercial_mono.wav"
    )
    args = parser.parse_args()

    sample_recognize(args.local_file_path)


if __name__ == "__main__":
    main()
