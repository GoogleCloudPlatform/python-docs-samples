# Copyright 2023 Google LLC
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


import argparse

# [START speech_transcribe_chirp_auto_detect_language]

from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def transcribe_with_auto_detect_lang(
    project_id: str,
    audio_file: str,
    region: str = "us-central1",
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file and auto-detect spoken language using Chirp."""
    # Instantiates a client
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{region}-speech.googleapis.com",
        )
    )

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["auto"], # Set language code to auto to detect language.
        model="chirp",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/{region}/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Detected Language: {result.language_code}")

    return response
