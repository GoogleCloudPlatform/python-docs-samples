# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Generated code. DO NOT EDIT!
#
# Snippet for StreamingRecognize
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-speech


# [START speech_v1p1beta1_generated_Speech_StreamingRecognize_sync]
from google.cloud import speech_v1p1beta1


def sample_streaming_recognize():
    # Create a client
    client = speech_v1p1beta1.SpeechClient()

    # Initialize request argument(s)
    streaming_config = speech_v1p1beta1.StreamingRecognitionConfig()
    streaming_config.config.language_code = "language_code_value"

    request = speech_v1p1beta1.StreamingRecognizeRequest(
        streaming_config=streaming_config,
    )

    # This method expects an iterator which contains
    # 'speech_v1p1beta1.StreamingRecognizeRequest' objects
    # Here we create a generator that yields a single `request` for
    # demonstrative purposes.
    requests = [request]

    def request_generator():
        for request in requests:
            yield request

    # Make the request
    stream = client.streaming_recognize(requests=request_generator())

    # Handle the response
    for response in stream:
        print(response)

# [END speech_v1p1beta1_generated_Speech_StreamingRecognize_sync]
