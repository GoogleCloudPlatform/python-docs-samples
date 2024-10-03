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

# [START speech_transcribe_override_recognizer]
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.protobuf.field_mask_pb2 import FieldMask

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def transcribe_override_recognizer(
    audio_file: str,
    recognizer_id: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file using an existing recognizer with overridden settings for the recognition request.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/audio.wav"
        recognizer_id (str): The unique ID of the recognizer to be used for transcription.
    Returns:
        cloud_speech.RecognizeResponse: The response containing the transcription results.
    """
    # Instantiates a client
    client = SpeechClient()

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
                    enable_word_time_offsets=True,
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
        config=cloud_speech.RecognitionConfig(
            features=cloud_speech.RecognitionFeatures(
                enable_word_time_offsets=False,
            ),
        ),
        config_mask=FieldMask(paths=["features.enable_word_time_offsets"]),
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_transcribe_override_recognizer]


if __name__ == "__main__":
    transcribe_override_recognizer(
        audio_file="resources/audio.wav", recognizer_id="id-recognizer"
    )
