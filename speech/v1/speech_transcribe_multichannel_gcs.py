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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_multichannel_gcs")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Multi-Channel Audio Transcription (Cloud Storage)
#   description: Transcribe a short audio file from Cloud Storage with multiple channels
#   usage: python3 samples/v1/speech_transcribe_multichannel_gcs.py [--storage_uri "gs://cloud-samples-data/speech/multi.wav"]

# [START speech_transcribe_multichannel_gcs]
from google.cloud import speech_v1


def sample_recognize(storage_uri):
    """
    Transcribe a short audio file from Cloud Storage with multiple channels

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/multi.wav'

    # The number of channels in the input audio file (optional)
    audio_channel_count = 2

    # When set to true, each audio channel will be recognized separately.
    # The recognition result will contain a channel_tag field to state which
    # channel that result belongs to
    enable_separate_recognition_per_channel = True

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "audio_channel_count": audio_channel_count,
        "enable_separate_recognition_per_channel": enable_separate_recognition_per_channel,
        "language_code": language_code,
    }
    audio = {"uri": storage_uri}

    response = client.recognize(config, audio)
    for result in response.results:
        # channel_tag to recognize which audio channel this result is for
        print(u"Channel tag: {}".format(result.channel_tag))
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_multichannel_gcs]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri", type=str, default="gs://cloud-samples-data/speech/multi.wav"
    )
    args = parser.parse_args()

    sample_recognize(args.storage_uri)


if __name__ == "__main__":
    main()
