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

"""Google Cloud Speech API sample that demonstrates how to select the model
used for speech recognition.
"""
from google.cloud import speech


def transcribe_model_selection() -> speech.RecognizeResponse:
    """Transcribe the given audio file synchronously with the selected model.
    List of possible models: https://cloud.google.com/speech-to-text/docs/transcription-model
    Returns:
        The response containing the transcription results.
    """
    # [START speech_transcribe_model_selection]
    from google.cloud import speech

    # Instantiates a client
    client = speech.SpeechClient()
    # Reads a file as bytes
    with open("resources/Google_Gnome.wav", "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="video",  # Chosen model
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")

    # [END speech_transcribe_model_selection]

    return response


def transcribe_model_selection_gcs() -> speech.RecognizeResponse:
    """Transcribe the given audio file synchronously with the selected model.
    List of possible models: https://cloud.google.com/speech-to-text/docs/transcription-model
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """
    # [START speech_transcribe_model_selection_gcs]
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(
        uri="gs://cloud-samples-tests/speech/Google_Gnome.wav"
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="video",  # Chosen model
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")

    # [END speech_transcribe_model_selection_gcs]
    return response
