# Copyright 2022 Google LLC
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


# [START speech_adaptation_v2_inline_phrase_set]
import io

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def adaptation_v2_inline_phrase_set(project_id, recognizer_id, audio_file):
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

    # Build inline phrase set to produce a more accurate transcript
    phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "fare", "boost": 10}])
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                inline_phrase_set=phrase_set
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


# [END speech_adaptation_v2_inline_phrase_set]


if __name__ == "__main__":
    adaptation_v2_inline_phrase_set()
