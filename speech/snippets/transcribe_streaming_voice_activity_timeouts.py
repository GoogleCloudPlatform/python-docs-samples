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


import argparse

# [START speech_transcribe_streaming_voice_activity_timeouts]
import io
from time import sleep

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.protobuf import duration_pb2  # type: ignore


def transcribe_streaming_voice_activity_timeouts(
    project_id, recognizer_id, speech_start_timeout, speech_end_timeout, audio_file
):
    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{project_id}/locations/global",
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            language_codes=["en-US"], model="latest_long"
        ),
    )

    # Creates a Recognizer
    operation = client.create_recognizer(request=request)
    recognizer = operation.result()

    # Reads a file as bytes
    with io.open(audio_file, "rb") as f:
        content = f.read()

    # In practice, stream should be a generator yielding chunks of audio data
    chunk_length = len(content) // 20
    stream = [
        content[start : start + chunk_length]
        for start in range(0, len(content), chunk_length)
    ]
    audio_requests = (
        cloud_speech.StreamingRecognizeRequest(audio=audio) for audio in stream
    )

    recognition_config = cloud_speech.RecognitionConfig(auto_decoding_config={})

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
        recognizer=recognizer.name, streaming_config=streaming_config
    )

    def requests(config, audio):
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
            print("Transcript: {}".format(result.alternatives[0].transcript))

    return responses


# [END speech_transcribe_streaming_voice_activity_timeouts]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="project to create recognizer in")
    parser.add_argument("recognizer_id", help="name of recognizer to create")
    parser.add_argument(
        "speech_start_timeout", help="timeout in seconds for speech start"
    )
    parser.add_argument("speech_end_timeout", help="timeout in seconds for speech end")
    parser.add_argument("audio_file", help="audio file to stream")
    args = parser.parse_args()
    transcribe_streaming_voice_activity_timeouts(
        args.project_id,
        args.recognizer_id,
        args.speech_start_timeout,
        args.speech_end_timeout,
        args.audio_file,
    )
