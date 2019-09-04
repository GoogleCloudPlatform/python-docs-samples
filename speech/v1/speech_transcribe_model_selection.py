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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_model_selection")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Selecting a Transcription Model (Local File)
#   description: Transcribe a short audio file using a specified transcription model
#   usage: python3 samples/v1/speech_transcribe_model_selection.py [--local_file_path "resources/hello.wav"] [--model "phone_call"]

# [START speech_transcribe_model_selection]
from google.cloud import speech_v1
import io


def sample_recognize(local_file_path, model):
    """
    Transcribe a short audio file using a specified transcription model

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
      model The transcription model to use, e.g. video, phone_call, default
      For a list of available transcription models, see:
      https://cloud.google.com/speech-to-text/docs/transcription-model#transcription_models
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/hello.wav'
    # model = 'phone_call'

    # The language of the supplied audio
    language_code = "en-US"
    config = {"model": model, "language_code": language_code}
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_model_selection]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--local_file_path", type=str, default="resources/hello.wav")
    parser.add_argument("--model", type=str, default="phone_call")
    args = parser.parse_args()

    sample_recognize(args.local_file_path, args.model)


if __name__ == "__main__":
    main()
