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


import argparse

# [START speech_adaptation_v2_inline_custom_class]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def adaptation_v2_inline_custom_class(
    project_id: str,
    audio_file: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe audio file using inline custom class

    Args:
        project_id: The GCP project ID.
        audio_file: The audio file to transcribe.

    Returns:
        The response from the recognizer.
    """
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    # Build inline phrase set to produce a more accurate transcript
    phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "${fare}", "boost": 20}])
    custom_class = cloud_speech.CustomClass(name="fare", items=[{"value": "fare"}])
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

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_adaptation_v2_inline_custom_class]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="GCP Project ID")
    parser.add_argument("audio_file", help="Audio file to stream")
    args = parser.parse_args()
    adaptation_v2_inline_custom_class(args.project_id, args.audio_file)
