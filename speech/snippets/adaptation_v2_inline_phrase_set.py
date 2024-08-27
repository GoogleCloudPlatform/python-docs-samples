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

# [START speech_adaptation_v2_inline_phrase_set]
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def adaptation_v2_inline_phrase_set(audio_file: str) -> cloud_speech.RecognizeResponse:
    """Enhances speech recognition accuracy using an inline phrase set.
    The inline custom phrase set helps the recognizer produce more accurate transcriptions for specific terms.
    Phrases are given a boost to increase their chances of being recognized correctly.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """

    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    # Build inline phrase set to produce a more accurate transcript
    phrase_set = cloud_speech.PhraseSet(
        phrases=[{"value": "fare", "boost": 10}, {"value": "word", "boost": 20}]
    )
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                inline_phrase_set=phrase_set
            )
        ]
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
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_adaptation_v2_inline_phrase_set]


if __name__ == "__main__":
    adaptation_v2_inline_phrase_set("resources/fair.wav")
