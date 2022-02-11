# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
# Snippet for Recognize
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-speech


# [START speech_generated_speech_v1p1beta1_Speech_Recognize_async]
from google.cloud import speech_v1p1beta1


async def sample_recognize():
    # Create a client
    client = speech_v1p1beta1.SpeechAsyncClient()

    # Initialize request argument(s)
    config = speech_v1p1beta1.RecognitionConfig()
    config.language_code = "language_code_value"

    audio = speech_v1p1beta1.RecognitionAudio()
    audio.content = b'content_blob'

    request = speech_v1p1beta1.RecognizeRequest(
        config=config,
        audio=audio,
    )

    # Make the request
    response = await client.recognize(request=request)

    # Handle the response
    print(response)

# [END speech_generated_speech_v1p1beta1_Speech_Recognize_async]
