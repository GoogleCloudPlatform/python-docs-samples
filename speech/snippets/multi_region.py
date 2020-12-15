#!/usr/bin/env python

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def sync_recognize_with_multi_region_gcs():
    # [START speech_multi_region]

    # Imports the Google Cloud client library
    from google.cloud import speech
    from google.api_core import client_options

    # Instantiates a client

    # [START speech_multi_region_client]

    # Pass an additional argument, ClientOptions, to specify the new endpoint.
    client_options = client_options.ClientOptions(
        api_endpoint="eu-speech.googleapis.com"
    )

    client = speech.SpeechClient(client_options=client_options)
    # [END speech_multi_region_client]

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
    # [END speech_multi_region]


sync_recognize_with_multi_region_gcs()
