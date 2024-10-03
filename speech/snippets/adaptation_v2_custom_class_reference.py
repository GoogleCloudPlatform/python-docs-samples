# Copyright 2022 Google LLC
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

# [START speech_adaptation_v2_custom_class_reference]
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def adaptation_v2_custom_class_reference(
    audio_file: str, phrase_set_id: str, custom_class_id: str
) -> cloud_speech.RecognizeResponse:
    """Transcribe audio file using a custom class.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
        phrase_set_id (str): The unique ID of the phrase set to use.
        custom_class_id (str): The unique ID of the custom class to use.
    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Instantiates a speech client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    # Create a custom class to improve recognition accuracy for specific terms
    custom_class = cloud_speech.CustomClass(items=[{"value": "fare"}])
    operation = client.create_custom_class(
        parent=f"projects/{PROJECT_ID}/locations/global",
        custom_class_id=custom_class_id,
        custom_class=custom_class,
    )
    custom_class = operation.result()

    # Create a persistent PhraseSet to reference in a recognition request
    created_phrase_set = cloud_speech.PhraseSet(
        phrases=[
            {
                "value": f"${{{custom_class.name}}}",
                "boost": 20,
            },  # Using custom class reference
        ]
    )
    operation = client.create_phrase_set(
        parent=f"projects/{PROJECT_ID}/locations/global",
        phrase_set_id=phrase_set_id,
        phrase_set=created_phrase_set,
    )
    phrase_set = operation.result()

    # Add a reference of the PhraseSet into the recognition request
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                phrase_set=phrase_set.name
            )
        ]
    )
    # Automatically detect the audio's encoding with short audio model
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        adaptation=adaptation,
        language_codes=["en-US"],
        model="short",
    )

    # Create a custom class to reference in a PhraseSet
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_adaptation_v2_custom_class_reference]


if __name__ == "__main__":
    adaptation_v2_custom_class_reference(
        audio_file="resources/fair.wav",
        phrase_set_id="custom-phrase-set",
        custom_class_id="custom-class-id",
    )
