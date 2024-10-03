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

# [START speech_transcribe_streaming_voice_activity_events]
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def transcribe_streaming_voice_activity_events(
    audio_file: str,
) -> cloud_speech.StreamingRecognizeResponse:
    """Transcribes audio from a file into text and detects voice activity
        events using Google Cloud Speech-to-Text API.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/audio.wav"
    Returns:
        list[cloud_speech.StreamingRecognizeResponse]: A list of `StreamingRecognizeResponse` objects.
    """
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as file:
        audio_content = file.read()

    # In practice, stream should be a generator yielding chunks of audio data
    chunk_length = len(audio_content) // 5
    stream = [
        audio_content[start : start + chunk_length]
        for start in range(0, len(audio_content), chunk_length)
    ]
    audio_requests = (
        cloud_speech.StreamingRecognizeRequest(audio=audio) for audio in stream
    )

    recognition_config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )

    # Sets the flag to enable voice activity events
    streaming_features = cloud_speech.StreamingRecognitionFeatures(
        enable_voice_activity_events=True
    )
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config, streaming_features=streaming_features
    )

    config_request = cloud_speech.StreamingRecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        streaming_config=streaming_config,
    )

    def requests(config: cloud_speech.RecognitionConfig, audio: list) -> list:
        yield config
        yield from audio

    # Transcribes the audio into text
    responses_iterator = client.streaming_recognize(
        requests=requests(config_request, audio_requests)
    )
    responses = []
    for response in responses_iterator:
        responses.append(response)
        if (
            response.speech_event_type
            == cloud_speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_ACTIVITY_BEGIN
        ):
            print("Speech started.")
        if (
            response.speech_event_type
            == cloud_speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_ACTIVITY_END
        ):
            print("Speech ended.")
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

    return responses


# [END speech_transcribe_streaming_voice_activity_events]


if __name__ == "__main__":
    transcribe_streaming_voice_activity_events("resources/audio.wav")
