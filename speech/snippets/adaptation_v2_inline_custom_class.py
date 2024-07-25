# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
RESOURCES_FOLDER = os.path.join(os.path.dirname(__file__), "resources")

# [START speech_adaptation_v2_inline_custom_class]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def adaptation_v2_inline_custom_class() -> cloud_speech.RecognizeResponse:
    """Transcribe audio file using inline custom class.
    The inline custom class helps the recognizer produce more accurate transcriptions for specific terms.

    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Instantiates a client
    client = SpeechClient()

    # Could be "resources/fair.wav" or any another absolute|relative path to the audio file
    audio_file = os.path.join(RESOURCES_FOLDER, "fair.wav")
    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    # Define an inline custom class with specific items to enhance recognition
    # The CustomClass is created with a specific value ("fare") that can be used
    #   to improve recognition accuracy for specific terms.
    custom_class_name = "your-class-name"
    custom_class = cloud_speech.CustomClass(
        name=custom_class_name,
        items=[{"value": "fare"}],
    )

    # Build inline phrase set to produce a more accurate transcript
    phrase_set = cloud_speech.PhraseSet(
        phrases=[{"value": custom_class_name, "boost": 20}]
    )
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                inline_phrase_set=phrase_set
            )
        ],
        custom_classes=[custom_class],
    )
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        adaptation=adaptation,
        language_codes=["en-US"],
        model="short",
    )

    # Prepare the request which includes specifying the recognizer, configuration, and the audio content
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text. The response contains the transcription results
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_adaptation_v2_inline_custom_class]


if __name__ == "__main__":
    recognition_response = adaptation_v2_inline_custom_class()
