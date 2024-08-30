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

# [START speech_transcribe_streaming_voice_activity_timeouts]
import os
from time import sleep

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.protobuf import duration_pb2  # type: ignore

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def transcribe_streaming_voice_activity_timeouts(
    speech_start_timeout: int,
    speech_end_timeout: int,
    audio_file: str,
) -> cloud_speech.StreamingRecognizeResponse:
    """Transcribes audio from audio file to text.
    Args:
        speech_start_timeout: The timeout in seconds for speech start.
        speech_end_timeout: The timeout in seconds for speech end.
        audio_file: Path to the local audio file to be transcribed.
            Example: "resources/audio_silence_padding.wav"
    Returns:
        The streaming response containing the transcript.
    """
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as file:
        audio_content = file.read()

    # In practice, stream should be a generator yielding chunks of audio data
    chunk_length = len(audio_content) // 20
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

    # Sets the flag to enable voice activity events and timeout
    speech_start_timeout = duration_pb2.Duration(seconds=speech_start_timeout)
    speech_end_timeout = duration_pb2.Duration(seconds=speech_end_timeout)
    voice_activity_timeout = (
        cloud_speech.StreamingRecognitionFeatures.VoiceActivityTimeout(
            speech_start_timeout=speech_start_timeout,
            speech_end_timeout=speech_end_timeout,
        )
    )
    streaming_features = cloud_speech.StreamingRecognitionFeatures(
        enable_voice_activity_events=True, voice_activity_timeout=voice_activity_timeout
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
        for message in audio:
            sleep(0.5)
            yield message

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


# [END speech_transcribe_streaming_voice_activity_timeouts]


if __name__ == "__main__":
    # Define the timeout duration for detecting the start of speech
    # In this case this means the function will wait for up to 5 seconds to determine if speech has started
    #   before it begins processing the audio stream.
    speech_start_timeout = 5
    # Define the timeout duration for detecting the end of speech
    # This indicates that the function will continue to listen for up to 1 second
    #     after the last detected speech segment to determine if speech has ended.
    speech_end_timeout = 1
    transcribe_streaming_voice_activity_timeouts(
        speech_start_timeout=speech_start_timeout,
        speech_end_timeout=speech_end_timeout,
        audio_file="resources/audio_silence_padding.wav",
    )
