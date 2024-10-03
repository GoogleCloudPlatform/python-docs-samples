# Copyright 2019 Google LLC
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

"""Google Cloud Speech API sample that demonstrates multichannel recognition.
"""

# [START speech_transcribe_multichannel]

from google.cloud import speech


def transcribe_file_with_multichannel(audio_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file synchronously with multi channel.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/multi.wav"
    Returns:
         cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    client = speech.SpeechClient()

    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")
        print(f"Channel Tag: {result.channel_tag}")

    return result
    # [END speech_transcribe_multichannel]


def transcribe_gcs_with_multichannel(audio_uri: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file from Google Cloud Storage synchronously with multichannel.
    Args:
        audio_uri (str): The Cloud Storage URI of the input audio.
            E.g., gs://cloud-samples-data/speech/multi.wav
    Returns:
        speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # [START speech_transcribe_multichannel_gcs]
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=audio_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")
        print(f"Channel Tag: {result.channel_tag}")

    return result
    # [END speech_transcribe_multichannel_gcs]


if __name__ == "__main__":
    # It could be a local path like: path_to_file = "resources/multi.wav"
    path_to_file = "gs://cloud-samples-data/speech/multi.wav"
    if path_to_file.startswith("gs://"):
        transcribe_gcs_with_multichannel(path_to_file)
    else:
        transcribe_file_with_multichannel(path_to_file)
