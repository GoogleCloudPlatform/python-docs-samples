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

import os

from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def transcribe_model_selection_v2() -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file using a specified speech recognition model.
        Available models: https://cloud.google.com/speech-to-text/v2/docs/transcription-model
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """
    # [START speech_transcribe_model_selection_v2]
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech

    # Instantiates a client
    client = SpeechClient()

    # TODO (Developer): Update the PROJECT_ID to the value of your project
    # PROJECT_ID = "your-project-id"

    # Reads a file as bytes
    with open("resources/audio.wav", "rb") as f:
        audio_content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="short",  # Chosen model
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    # [END speech_transcribe_model_selection_v2]

    return response
