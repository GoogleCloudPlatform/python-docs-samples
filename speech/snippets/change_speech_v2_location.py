# Copyright 2024 Google LLC
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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# [START speech_change_speech_v2_location]
from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def change_speech_v2_location(
    location: str,
    audio_file: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file in a specific region. It allows for specifying the location
        to potentially reduce latency and meet data residency requirements.
    Args:
        location (str): The cloud region where the Speech-to-Text API is called.
            For example, 'europe-west3'.
            Use 'gcloud compute regions list' for available locations
        audio_file (str): The path to the audio file to be transcribed.
    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
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

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/{location}/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
    return response


# [END speech_change_speech_v2_location]

if __name__ == "__main__":
    path_to_audio_file = "resources/audio.wav"
    api_location = "europe-west3"
    change_speech_v2_location(api_location, path_to_audio_file)
