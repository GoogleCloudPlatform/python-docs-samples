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
import io

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def adaptation_v2_custom_class_reference(
    project_id, recognizer_id, phrase_set_id, custom_class_id, audio_file
):
    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{project_id}/locations/global",
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            language_codes=["en-US"], model="latest_short"
        ),
    )

    # Creates a Recognizer
    operation = client.create_recognizer(request=request)
    recognizer = operation.result()

    # Reads a file as bytes
    with io.open(audio_file, "rb") as f:
        content = f.read()

    # Create a persistent CustomClass to reference in phrases
    request = cloud_speech.CreateCustomClassRequest(
        parent=f"projects/{project_id}/locations/global",
        custom_class_id=custom_class_id,
        custom_class=cloud_speech.CustomClass(items=[{"value": "fare"}]),
    )

    operation = client.create_custom_class(request=request)
    custom_class = operation.result()

    # Create a persistent PhraseSet to reference in a recognition request
    request = cloud_speech.CreatePhraseSetRequest(
        parent=f"projects/{project_id}/locations/global",
        phrase_set_id=phrase_set_id,
        phrase_set=cloud_speech.PhraseSet(
            phrases=[{"value": f"${{{custom_class.name}}}", "boost": 20}]
        ),
    )

    operation = client.create_phrase_set(request=request)
    phrase_set = operation.result()

    # Add a reference of the PhraseSet into the recognition request
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                phrase_set=phrase_set.name
            )
        ]
    )
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config={}, adaptation=adaptation
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=recognizer.name, config=config, content=content
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

    return response


# [END speech_adaptation_v2_custom_class_reference]


if __name__ == "__main__":
    adaptation_v2_custom_class_reference()
