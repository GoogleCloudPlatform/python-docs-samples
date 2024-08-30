# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.
"""

from google.cloud import speech


# [START speech_transcribe_streaming]
def transcribe_streaming(stream_file: str) -> speech.RecognitionConfig:
    """Streams transcription of the given audio file using Google Cloud Speech-to-Text API.
    Args:
        stream_file (str): Path to the local audio file to be transcribed.
            Example: "resources/audio.raw"
    """
    client = speech.SpeechClient()

    # [START speech_python_migration_streaming_request]
    with open(stream_file, "rb") as audio_file:
        audio_content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [audio_content]

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    # [START speech_python_migration_streaming_response]
    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )
    # [END speech_python_migration_streaming_request]

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print(f"Finished: {result.is_final}")
            print(f"Stability: {result.stability}")
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print(f"Confidence: {alternative.confidence}")
                print(f"Transcript: {alternative.transcript}")

    # [END speech_python_migration_streaming_response]


# [END speech_transcribe_streaming]


if __name__ == "__main__":
    transcribe_streaming("resources/audio.raw")
