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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_multilanguage_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Detecting language spoken automatically (Local File) (Beta)
#   description: Transcribe a short audio file with language detected from a list of possible
#     languages
#   usage: python3 samples/v1p1beta1/speech_transcribe_multilanguage_beta.py [--local_file_path "resources/brooklyn_bridge.flac"]

# [START speech_transcribe_multilanguage_beta]
from google.cloud import speech_v1p1beta1
import io


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file with language detected from a list of possible
    languages

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.flac'

    # The language of the supplied audio. Even though additional languages are
    # provided by alternative_language_codes, a primary language is still required.
    language_code = "fr"

    # Specify up to 3 additional languages as possible alternative languages
    # of the supplied audio.
    alternative_language_codes_element = "es"
    alternative_language_codes_element_2 = "en"
    alternative_language_codes = [
        alternative_language_codes_element,
        alternative_language_codes_element_2,
    ]
    config = {
        "language_code": language_code,
        "alternative_language_codes": alternative_language_codes,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # The language_code which was detected as the most likely being spoken in the audio
        print(u"Detected language: {}".format(result.language_code))
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_multilanguage_beta]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local_file_path", type=str, default="resources/brooklyn_bridge.flac"
    )
    args = parser.parse_args()

    sample_recognize(args.local_file_path)


if __name__ == "__main__":
    main()
