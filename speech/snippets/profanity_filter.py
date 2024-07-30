# Copyright 2024 Google LLC
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

""" Google Cloud Speech API sample application using the REST API for batch
processing.
"""
from google.cloud.speech import RecognizeResponse


def sync_recognize_with_profanity_filter_gcs() -> RecognizeResponse:
    """Recognizes speech from an audio file in Cloud Storage and filters out profane language.

    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # [START speech_recognize_with_profanity_filter_gcs]
    from google.cloud import speech

    # Replace with the URI of your audio file in Google Cloud Storage
    audio_uri = "gs://cloud-samples-tests/speech/brooklyn.flac"
    # Define the audio source
    audio = {"uri": audio_uri}

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,  # Audio format
        sample_rate_hertz=16000,
        language_code="en-US",
        profanity_filter=True,  # Enable profanity filter
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")

    # [END speech_recognize_with_profanity_filter_gcs]

    return response.results


if __name__ == "__main__":
    recognition_response = sync_recognize_with_profanity_filter_gcs()
