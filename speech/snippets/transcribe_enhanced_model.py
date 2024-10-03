# Copyright 2018 Google LLC
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

"""Google Cloud Speech API sample that demonstrates enhanced models
and recognition metadata.
"""
# [START speech_transcribe_enhanced_model]

from google.cloud import speech


def transcribe_file_with_enhanced_model(audio_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file using an enhanced model.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/commercial_mono.wav"
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """

    client = speech.SpeechClient()

    # audio_file = 'resources/commercial_mono.wav'
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model="phone_call",
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")

    return response
    # [END speech_transcribe_enhanced_model]


if __name__ == "__main__":
    transcribe_file_with_enhanced_model("resources/commercial_mono.wav")
