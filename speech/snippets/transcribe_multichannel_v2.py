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

# [START speech_transcribe_multichannel_v2]
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def transcribe_multichannel_v2(
    audio_file: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe the given audio file synchronously with multichannel.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/two_channel_16k.wav"
    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
        features=cloud_speech.RecognitionFeatures(
            multi_channel_mode=cloud_speech.RecognitionFeatures.MultiChannelMode.SEPARATE_RECOGNITION_PER_CHANNEL,
        ),
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Channel tag: {result.channel_tag}")

    return response


# [END speech_transcribe_multichannel_v2]


if __name__ == "__main__":
    transcribe_multichannel_v2("resources/two_channel_16k.wav")
