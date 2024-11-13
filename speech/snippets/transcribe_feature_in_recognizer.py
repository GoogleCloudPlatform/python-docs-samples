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


def transcribe_feature_in_recognizer(
    audio_file: str,
    recognizer_id: str,
) -> cloud_speech.RecognizeResponse:
    """Use an existing recognizer or create a new one to transcribe an audio file.
    Args:
        audio_file (str): The path to the audio file to be transcribed.
            Example: "resources/audio.wav"
        recognizer_id (str): The ID of the recognizer to be used or created. ID should be unique
            within the project and location.
    Returns:
        cloud_speech.RecognizeResponse: The response containing the transcription results.
    """
    # [START speech_transcribe_feature_in_recognizer]

    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech

    from google.api_core.exceptions import NotFound

    # Instantiates a client
    client = SpeechClient()

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    # recognizer_id = "id-recognizer"
    recognizer_name = (
        f"projects/{PROJECT_ID}/locations/global/recognizers/{recognizer_id}"
    )
    try:
        # Use an existing recognizer
        recognizer = client.get_recognizer(name=recognizer_name)
        print("Using existing Recognizer:", recognizer.name)
    except NotFound:
        # Create a new recognizer
        request = cloud_speech.CreateRecognizerRequest(
            parent=f"projects/{PROJECT_ID}/locations/global",
            recognizer_id=recognizer_id,
            recognizer=cloud_speech.Recognizer(
                default_recognition_config=cloud_speech.RecognitionConfig(
                    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                    language_codes=["en-US"],
                    model="latest_long",
                    features=cloud_speech.RecognitionFeatures(
                        enable_automatic_punctuation=True,
                    ),
                ),
            ),
        )
        operation = client.create_recognizer(request=request)
        recognizer = operation.result()
        print("Created Recognizer:", recognizer.name)

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/{recognizer_id}",
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    # [END speech_transcribe_feature_in_recognizer]

    return response


if __name__ == "__main__":
    transcribe_feature_in_recognizer(
        audio_file="resources/audio.wav", recognizer_id="id-recognizer"
    )
