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


import argparse

# [START speech_transcribe_feature_in_recognizer]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def transcribe_feature_in_recognizer(
    project_id: str,
    recognizer_id: str,
    audio_file: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file using an existing recognizer."""
    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{project_id}/locations/global",
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
        content = f.read()

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/{recognizer_id}",
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_transcribe_feature_in_recognizer]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="GCP Project ID")
    parser.add_argument("recognizer_id", help="Recognizer ID to use for recogniition")
    parser.add_argument("audio_file", help="Audio file to stream")
    args = parser.parse_args()
    transcribe_feature_in_recognizer(args.project_id, args.audio_file)
