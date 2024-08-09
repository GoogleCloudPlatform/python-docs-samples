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

# [START speech_transcribe_model_selection]
from google.cloud import speech


def transcribe_model_selection(
    audio_file: str,
    model: str,
) -> speech.RecognizeResponse:
    """Transcribe the given audio file synchronously with the selected model.
    List of possible models: https://cloud.google.com/speech-to-text/docs/transcription-model
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/fair.wav"
        model (str): The model to be used for transcription.
            Example: "phone_call".
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """
    # Instantiates a client
    client = speech.SpeechClient()
    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,  # Chosen model
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")

    return response


# [END speech_transcribe_model_selection]


# [START speech_transcribe_model_selection_gcs]


def transcribe_model_selection_gcs(
    audio_uri: str,
    model: str,
) -> speech.RecognizeResponse:
    """Transcribe the given audio file synchronously with the selected model.
    List of possible models: https://cloud.google.com/speech-to-text/docs/transcription-model
    Args:
        audio_uri (str): The Cloud Storage URI of the input audio.
            e.g., gs://[BUCKET]/[FILE]
        model (str): The model to be used for transcription.
            Example: "phone_call" or "video"
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=audio_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")

    return response


# [END speech_transcribe_model_selection_gcs]


if __name__ == "__main__":
    # It could be a local path like: path_to_file = "resources/Google_Gnome.wav"
    path_to_file = "gs://cloud-samples-tests/speech/Google_Gnome.wav"
    # Possible models: "command_and_search", "phone_call", "video", "default"
    model = "phone_call"

    if path_to_file.startswith("gs://"):
        transcribe_model_selection_gcs(path_to_file, model)
    else:
        transcribe_model_selection(path_to_file, model)
