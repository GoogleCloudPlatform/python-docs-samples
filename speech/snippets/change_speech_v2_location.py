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


# [START speech_change_speech_v2_location]
import os

from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def change_speech_v2_location(
    audio_file: str, location: str
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file in a specific region. It allows for specifying the location
        to potentially reduce latency and meet data residency requirements.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
        location (str): The region where the Speech API will be accessed.
            E.g., "europe-west3"
    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    # Instantiates a client to a regionalized Speech endpoint.
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-speech.googleapis.com",
        )
    )

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/{location}/recognizers/_",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
    return response


# [END speech_change_speech_v2_location]

if __name__ == "__main__":
    change_speech_v2_location(audio_file="resources/audio.wav", location="us-central1")
