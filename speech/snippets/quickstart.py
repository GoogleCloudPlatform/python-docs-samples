# Copyright 2016 Google LLC
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

# [START speech_quickstart]

# Imports the Google Cloud client library

# [START speech_python_migration_imports]

from google.cloud import speech

# [END speech_python_migration_imports]


def run_quickstart(audio_uri: str) -> speech.RecognizeResponse:
    # Instantiates a client
    # [START speech_python_migration_client]
    client = speech.SpeechClient()
    # [END speech_python_migration_client]

    audio = speech.RecognitionAudio(uri=audio_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
    # [END speech_quickstart]

    return response


if __name__ == "__main__":
    # Replace with the URI of your audio file in Google Cloud Storage
    audio_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
    run_quickstart(audio_uri)
