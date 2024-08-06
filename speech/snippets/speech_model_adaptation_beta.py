# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START speech_transcribe_with_model_adaptation]
import os

from google.cloud import speech_v1p1beta1 as speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def transcribe_with_model_adaptation(
    audio_uri: str,
    custom_class_id: str,
    phrase_set_id: str,
) -> str:
    """Create `PhraseSet` and `CustomClasses` for custom item lists in input data.
    Args:
        audio_uri (str): The Cloud Storage URI of the input audio. e.g. gs://[BUCKET]/[FILE]
        custom_class_id (str): The unique ID of the custom class to create
        phrase_set_id (str): The unique ID of the PhraseSet to create.
    Returns:
        The transcript of the input audio.
    """
    # Specifies the location where the Speech API will be accessed.
    location = "global"

    # Audio object
    audio = speech.RecognitionAudio(uri=audio_uri)

    # Create the adaptation client
    adaptation_client = speech.AdaptationClient()

    # The parent resource where the custom class and phrase set will be created.
    parent = f"projects/{PROJECT_ID}/locations/{location}"

    # Create the custom class resource
    adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": custom_class_id,
            "custom_class": {
                "items": [
                    {"value": "sushido"},
                    {"value": "altura"},
                    {"value": "taneda"},
                ]
            },
        }
    )
    custom_class_name = (
        f"projects/{PROJECT_ID}/locations/{location}/customClasses/{custom_class_id}"
    )
    # Create the phrase set resource
    phrase_set_response = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": phrase_set_id,
            "phrase_set": {
                "boost": 10,
                "phrases": [
                    {"value": f"Visit restaurants like ${{{custom_class_name}}}"}
                ],
            },
        }
    )
    phrase_set_name = phrase_set_response.name
    # The next section shows how to use the newly created custom
    # class and phrase set to send a transcription request with speech adaptation

    # Speech adaptation configuration
    speech_adaptation = speech.SpeechAdaptation(phrase_set_references=[phrase_set_name])

    # speech configuration object
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code="en-US",
        adaptation=speech_adaptation,
    )

    # Create the speech client
    speech_client = speech.SpeechClient()

    response = speech_client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    # [END speech_transcribe_with_model_adaptation]

    return response.results[0].alternatives[0].transcript


if __name__ == "__main__":
    transcribe_with_model_adaptation(
        audio_uri="gs://cloud-samples-data/speech/brooklyn_bridge.raw",
        custom_class_id="your-custom-class-id",
        phrase_set_id="your-phrase-set-id",
    )
