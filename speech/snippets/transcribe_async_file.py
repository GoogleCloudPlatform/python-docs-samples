# Copyright 2021 Google LLC
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

"""Google Cloud Speech-to-Text sample application using gRPC for async
batch processing.
"""


# [START speech_transcribe_async]
from google.cloud import speech


def transcribe_file(audio_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file asynchronously.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
    """
    client = speech.SpeechClient()

    # [START speech_python_migration_async_request]
    with open(audio_file, "rb") as file:
        audio_content = file.read()

    # Note that transcription is limited to a 60 seconds local audio file.
    # Use a GCS file for audio longer than 1 minute.
    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # [START speech_python_migration_async_response]

    operation = client.long_running_recognize(config=config, audio=audio)
    # [END speech_python_migration_async_request]

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Confidence: {result.alternatives[0].confidence}")
    # [END speech_python_migration_async_response]

    return response


# [END speech_transcribe_async]
if __name__ == "__main__":
    transcribe_file("resources/audio.raw")
