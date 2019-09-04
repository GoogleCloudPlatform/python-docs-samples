# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_word_level_confidence_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Enabling word-level confidence (Local File) (Beta)
#   description: Print confidence level for individual words in a transcription of a short audio
#     file.
#   usage: python3 samples/v1p1beta1/speech_transcribe_word_level_confidence_beta.py [--local_file_path "resources/brooklyn_bridge.flac"]

# [START speech_transcribe_word_level_confidence_beta]
from google.cloud import speech_v1p1beta1
import io


def sample_recognize(local_file_path):
    """
    Print confidence level for individual words in a transcription of a short audio
    file.

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.flac'

    # When enabled, the first result returned by the API will include a list
    # of words and the confidence level for each of those words.
    enable_word_confidence = True

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "enable_word_confidence": enable_word_confidence,
        "language_code": language_code,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    # The first result includes confidence levels per word
    result = response.results[0]
    # First alternative is the most probable result
    alternative = result.alternatives[0]
    print(u"Transcript: {}".format(alternative.transcript))
    # Print the confidence level of each word
    for word in alternative.words:
        print(u"Word: {}".format(word.word))
        print(u"Confidence: {}".format(word.confidence))


# [END speech_transcribe_word_level_confidence_beta]


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
