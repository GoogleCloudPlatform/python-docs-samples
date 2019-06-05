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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_contexts_classes_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title:
#   description: Performs synchronous speech recognition with static context classes.
#   usage: python3 samples/v1p1beta1/speech_contexts_classes_beta.py [--sample_rate_hertz 24000] [--language_code "en-US"] [--phrase "$TIME"] [--uri_path "gs://cloud-samples-data/speech/time.mp3"]
import sys

# [START speech_contexts_classes_beta]

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import six


def sample_recognize(sample_rate_hertz, language_code, phrase, uri_path):
    """
    Performs synchronous speech recognition with static context classes.

    Args:
      sample_rate_hertz Sample rate in Hertz of the audio data sent in all
      `RecognitionAudio` messages. Valid values are: 8000-48000.
      language_code The language of the supplied audio.
      phrase Phrase "hints" help Speech-to-Text API recognize the specified phrases
      from your audio data. In this sample we are using a static class phrase
      ($TIME). Classes represent groups of words that represent common concepts that
      occur in natural language. We recommend checking out the docs page for more
      info on static classes.
      uri_path Path to the audio file stored on GCS.
    """
    # [START speech_contexts_classes_beta_core]

    client = speech_v1p1beta1.SpeechClient()

    # sample_rate_hertz = 24000
    # language_code = 'en-US'
    # phrase = '$TIME'
    # uri_path = 'gs://cloud-samples-data/speech/time.mp3'

    if isinstance(language_code, six.binary_type):
        language_code = language_code.decode("utf-8")
    if isinstance(phrase, six.binary_type):
        phrase = phrase.decode("utf-8")
    if isinstance(uri_path, six.binary_type):
        uri_path = uri_path.decode("utf-8")
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    phrases = [phrase]
    speech_contexts_element = {"phrases": phrases}
    speech_contexts = [speech_contexts_element]
    config = {
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "speech_contexts": speech_contexts,
    }
    audio = {"uri": uri_path}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))

    # [END speech_contexts_classes_beta_core]


# [END speech_contexts_classes_beta]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_rate_hertz", type=int, default=24000)
    parser.add_argument("--language_code", type=str, default="en-US")
    parser.add_argument("--phrase", type=str, default="$TIME")
    parser.add_argument(
        "--uri_path", type=str, default="gs://cloud-samples-data/speech/time.mp3"
    )
    args = parser.parse_args()

    sample_recognize(
        args.sample_rate_hertz, args.language_code, args.phrase, args.uri_path
    )


if __name__ == "__main__":
    main()
